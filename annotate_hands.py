import cv2
import mediapipe as mp
import os

from gesture_mapping import gesture_mapping_vowels


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
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
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
        return

    # Prepare annotation file
    image_name = os.path.basename(image_path)
    annotation_path = os.path.join(output_dir, os.path.splitext(image_name)[0] + ".txt")
    os.makedirs(output_dir, exist_ok=True)

    with open(annotation_path, "w") as annotation_file:
        for hand_landmarks in results.multi_hand_landmarks:
            offset=25
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

    # Draw landmarks and bounding box for visualization (optional)
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

    # Save visualization (optional)
    visualized_path = os.path.join(output_dir, "visualized_" + image_name)
    cv2.imwrite(visualized_path, image)
    print(f"Visualization saved: {visualized_path}")

    # Release resources
    hands.close()


def batch_process_images(input_dir, output_dir, class_id=0):
    """
    Processes all images in a directory, detects hands, and creates YOLO annotations.

    Args:
        input_dir (str): Directory containing images.
        output_dir (str): Directory to save annotations.
        class_id (int): Class ID for the hand gesture.
    """
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all image files in the input directory
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        print("No image files found in the input directory.")
        return

    print(f"Processing {len(image_files)} images from {input_dir}")

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        detect_and_annotate(image_path, output_dir, class_id)


# Example usage
letter='I'
input_dir = f"Dataset/Images/NSL_Vowel/S1_NSL_Vowel_Unprepared_Bright/S1_{letter}"  # Replace with the folder containing images
output_dir = f"Dataset/Images/NSL_Vowel/S1_NSL_Vowel_Unprepared_Bright/S1_{letter}"  # Replace with the folder to save annotations
class_id = gesture_mapping_vowels[letter]  # Class ID for hand gestures to be changed for each gesture.
# maybe create a dictionary with key as character and value as class_id

batch_process_images(input_dir, output_dir, class_id)