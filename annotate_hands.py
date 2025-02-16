# heavy memory usage due to multiple mediapipe object creations,
# refer to annotate_hands_eff which uses single mediapipe object for entire process
import os
import random
import shutil
import cv2
import mediapipe as mp
from sklearn.model_selection import train_test_split

from gesture_mapping import gesture_mapping_vowels


def split_data(src_dir, dest_dir, train_size=0.7):
    """
    Split the dataset into train and test sets, maintaining class structure.

    Args:
        src_dir (str): Root directory containing class subdirectories with images.
        dest_dir (str): Destination directory to save the split data (train/test).
        train_size (float): Proportion of data to use for training.

    Returns:
        None
    """
    # Create train and test directories dynamically
    train_images_dir = os.path.join(dest_dir, 'train', 'train_images')
    test_images_dir = os.path.join(dest_dir, 'test', 'test_images')
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)

    # Loop through each subdirectory in src_dir
    for sub_dir in os.listdir(src_dir):
        sub_dir_path = os.path.join(src_dir, sub_dir)

        # Skip if it's not a directory
        if not os.path.isdir(sub_dir_path):
            continue

        # List all image files in the class directory
        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # Split the files into train and test using train_test_split
        train_files, test_files = train_test_split(image_files, train_size=train_size, random_state=42)

        # Create class subdirectories for each letter in train and test
        os.makedirs(os.path.join(train_images_dir, sub_dir), exist_ok=True)
        os.makedirs(os.path.join(test_images_dir, sub_dir), exist_ok=True)

        # Copy files from src/sub_dir to train/test directories
        for file in train_files:
            shutil.copy(os.path.join(sub_dir_path, file), os.path.join(train_images_dir, sub_dir, file))
        for file in test_files:
            shutil.copy(os.path.join(sub_dir_path, file), os.path.join(test_images_dir, sub_dir, file))


def detect_and_annotate(image_path, output_dir, class_id=0):
    """
    Detects hands in an image using MediaPipe and creates YOLO-style annotations.

    Args:
        image_path (str): Path to the image file.
        output_dir (str): Directory to save annotations.
        class_id (int): Class ID for the hand gesture.
    """
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.8)
    mp_drawing = mp.solutions.drawing_utils

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return

    height, width, _ = image.shape

    # Convert the image to RGB (MediaPipe requires RGB images)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        print(f"No hands detected in {image_path}")
        os.remove(image_path)
        return

    # Prepare annotation file
    image_name = os.path.basename(image_path)
    annotation_path = os.path.join(output_dir, os.path.splitext(image_name)[0] + ".txt")
    os.makedirs(output_dir, exist_ok=True)

    with open(annotation_path, "w") as annotation_file:
        for hand_landmarks in results.multi_hand_landmarks:
            offset = 30
            # Get bounding box from landmarks
            x_min = max(0, min([lm.x for lm in hand_landmarks.landmark]) * width - offset)
            y_min = max(0, min([lm.y for lm in hand_landmarks.landmark]) * height - offset)
            x_max = min(width, max([lm.x for lm in hand_landmarks.landmark]) * width + offset)
            y_max = min(height, max([lm.y for lm in hand_landmarks.landmark]) * height + offset)

            # Normalize coordinates
            x_center = ((x_min + x_max) / 2) / width
            y_center = ((y_min + y_max) / 2) / height
            box_width = (x_max - x_min) / width
            box_height = (y_max - y_min) / height

            # Write YOLO annotation
            annotation_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

    print(f"Annotations saved for {image_name}: {annotation_path}")

    # # Draw landmarks and bounding box for visualization (optional)
    # for hand_landmarks in results.multi_hand_landmarks:
    #     mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    #     cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
    #
    # # Save visualization (optional)
    # visualized_path = os.path.join(output_dir, "visualized_" + image_name)
    # cv2.imwrite(visualized_path, image)
    # print(f"Visualization saved: {visualized_path}")

    # Release resources
    hands.close()


def annotate_images(input_dir, output_dir):
    """
    Annotates all images in a directory with YOLO-style annotations using gesture mapping.

    Args:
        input_dir (str): Directory containing the images.
        output_dir (str): Directory to save the annotations.
    """
    # Loop through each class (subdirectory)
    for sub_dir in os.listdir(input_dir):
        sub_dir_path = os.path.join(input_dir, sub_dir)

        # Skip if it's not a directory
        if not os.path.isdir(sub_dir_path):
            continue

        # Get the class_id for this gesture
        class_id = gesture_mapping_vowels.get(sub_dir.split("_", 1)[1])
        if class_id is None:
            print(f"Warning: Gesture '{sub_dir}' not found in mapping. Skipping.")
            continue

        # Get all image files in the class directory
        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        # annotate_output_dir = os.path.join(output_dir, sub_dir)
        for image_file in image_files:
            image_path = os.path.join(sub_dir_path, image_file)
            annotate_output_dir = os.path.join(output_dir, sub_dir)
            detect_and_annotate(image_path, annotate_output_dir, class_id)

if __name__ == "__main__":
# Example usage:
    src_dir = "Dataset/Images/NSL_Vowel/S1_NSL_Vowel_Unprepared_Bright"     #group 1
    dest_dir = "Dataset/YOLO_Data_ver4"  # Directory where train and test will be saved

    # Split the data into train and test sets
    split_data(src_dir, dest_dir, train_size=0.7)

    # annotate_images(os.path.join(dest_dir, 'train', 'train_images'), os.path.join(dest_dir, 'train', 'train_annotations'))
    annotate_images(os.path.join(dest_dir, 'test', 'test_images'), os.path.join(dest_dir, 'test', 'test_annotations'))
