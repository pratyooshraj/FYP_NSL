import os
import cv2
import mediapipe as mp
from sklearn.model_selection import train_test_split
import shutil
from gesture_mapping import gesture_mapping_vowels


def split_data(src_dir, dest_dir, train_size=0.7):
    """Split the dataset into train and test sets, maintaining class structure."""
    train_dir = os.path.join(dest_dir, 'train', 'train_images')
    test_dir = os.path.join(dest_dir, 'test', 'test_images')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    for sub_dir in os.listdir(src_dir):
        sub_dir_path = os.path.join(src_dir, sub_dir)

        if not os.path.isdir(sub_dir_path):
            continue

        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        train_files, test_files = train_test_split(image_files, train_size=train_size, random_state=42)

        for file_set, save_dir in [(train_files, train_dir), (test_files, test_dir)]:
            class_save_dir = os.path.join(save_dir, sub_dir)
            os.makedirs(class_save_dir, exist_ok=True)
            for file in file_set:
                shutil.copy(os.path.join(sub_dir_path, file), os.path.join(class_save_dir, file))




def split_data(src_dir, dest_dir, train_size=0.8, val_size=0.1, test_size=0.1):
    """Split the dataset into train, validation, and test sets, maintaining class structure."""

    # Validate that the sum of train_size, val_size, and test_size is 1
    if train_size + val_size + test_size != 1.0:
        raise ValueError("The sum of train_size, val_size, and test_size must equal 1.0")

    # Create directories for train, validation, and test sets
    train_dir = os.path.join(dest_dir, 'train', 'train_images')
    val_dir = os.path.join(dest_dir, 'val', 'val_images')
    test_dir = os.path.join(dest_dir, 'test', 'test_images')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Loop through each class folder in the source directory
    for sub_dir in os.listdir(src_dir):
        sub_dir_path = os.path.join(src_dir, sub_dir)

        if not os.path.isdir(sub_dir_path):
            continue

        # Get list of image files in the current class folder
        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # Split data into train and remaining (val + test) set
        train_files, remaining_files = train_test_split(image_files, train_size=train_size, random_state=42)

        # Split remaining files into validation and test sets
        val_files, test_files = train_test_split(remaining_files, train_size=val_size / (val_size + test_size),
                                                 random_state=42)

        # Copy files into corresponding directories
        for file_set, save_dir in [(train_files, train_dir), (val_files, val_dir), (test_files, test_dir)]:
            class_save_dir = os.path.join(save_dir, sub_dir)
            os.makedirs(class_save_dir, exist_ok=True)
            for file in file_set:
                shutil.copy(os.path.join(sub_dir_path, file), os.path.join(class_save_dir, file))



def detect_and_annotate(image_path, output_dir, class_id, hands_processor, width, height):
    """Detect hands in an image and create YOLO-style annotations."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading {image_path}")
        return False

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands_processor.process(image_rgb)

    # if not results.multi_hand_landmarks:
    #     print(f"No hands detected in {image_path}")
    #     os.remove(image_path)
    #     return False
    if not results.multi_hand_landmarks:
        print(f"No hands detected in {image_path}")

        # Define the target directory for images with no hands detected
        hands_not_found_dir = os.path.join("dataset", "hands_not_found")
        os.makedirs(hands_not_found_dir, exist_ok=True)  # Ensure the directory exists

        # Move the image to the target directory
        target_path = os.path.join(hands_not_found_dir, os.path.basename(image_path))
        os.rename(image_path, target_path)  # Move the file
        print(f"Moved {image_path} to {target_path}")
        return False

    annotation_path = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + ".txt")
    os.makedirs(output_dir, exist_ok=True)

    with open(annotation_path, "w") as f:
        for hand_landmarks in results.multi_hand_landmarks:
            offset = 30
            x_min = max(0, min([lm.x for lm in hand_landmarks.landmark]) * width - offset)
            y_min = max(0, min([lm.y for lm in hand_landmarks.landmark]) * height - offset)
            x_max = min(width, max([lm.x for lm in hand_landmarks.landmark]) * width + offset)
            y_max = min(height, max([lm.y for lm in hand_landmarks.landmark]) * height + offset)

            x_center = ((x_min + x_max) / 2) / width
            y_center = ((y_min + y_max) / 2) / height
            box_width = (x_max - x_min) / width
            box_height = (y_max - y_min) / height

            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

    return True


def annotate_images(input_dir, output_dir):
    """Annotate all images in a directory with YOLO-style annotations."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.8)

    for sub_dir in os.listdir(input_dir):
        sub_dir_path = os.path.join(input_dir, sub_dir)

        if not os.path.isdir(sub_dir_path):
            continue

        class_id = gesture_mapping_vowels.get(sub_dir.split("_", 1)[1])
        if class_id is None:
            print(f"Warning: Gesture '{sub_dir}' not found in mapping. Skipping.")
            continue

        output_class_dir = os.path.join(output_dir, sub_dir)
        os.makedirs(output_class_dir, exist_ok=True)

        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        for image_file in image_files:
            image_path = os.path.join(sub_dir_path, image_file)
            image = cv2.imread(image_path)

            if image is None:
                continue

            height, width = image.shape[:2]
            detect_and_annotate(image_path, output_class_dir, class_id, hands, width, height)

    hands.close()


if __name__ == "__main__":
    src_dir = "Dataset/Images/NSL_Vowel/s1_nsl_vowel_unprepared_bright_2"
    dest_dir = "Dataset/YOLO_Data_ver5_2"

    # Split the data
    split_data(src_dir, dest_dir)

    # Annotate training and testing data
    annotate_images(os.path.join(dest_dir, 'train', 'train_images'), os.path.join(dest_dir, 'train', 'train_annotations'))
    annotate_images(os.path.join(dest_dir, 'test', 'test_images'), os.path.join(dest_dir, 'test', 'test_annotations'))
