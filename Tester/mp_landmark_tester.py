import os
import cv2
import mediapipe as mp
from gesture_mapping import gesture_mapping_vowels


def detect_and_annotate(image_path, output_dir, class_id, hands_processor, width, height):
    """Detect hands in an image and create YOLO-style annotations."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading {image_path}")
        return False

    # Convert image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands_processor.process(image_rgb)

    # If no hands detected, skip
    # if not results.multi_hand_landmarks:
    #     print(f"No hands detected in {image_path}")
    #     return False
    if not results.multi_hand_landmarks:
        print(f"No hands detected in {image_path}")

        # Define the target directory for images with no hands detected
        hands_not_found_dir = os.path.join("../Dataset", "hands_not_found")
        os.makedirs(hands_not_found_dir, exist_ok=True)  # Ensure the directory exists

        # Move the image to the target directory
        target_path = os.path.join(hands_not_found_dir, os.path.basename(image_path))
        os.rename(image_path, target_path)  # Move the file
        print(f"Moved {image_path} to {target_path}")
        return False

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Annotation file path
    annotation_path = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + ".txt")
    with open(annotation_path, "w") as f:
        for hand_landmarks in results.multi_hand_landmarks:
            offset = 30  # Padding for bounding box
            x_min = max(0, min([lm.x for lm in hand_landmarks.landmark]) * width - offset)
            y_min = max(0, min([lm.y for lm in hand_landmarks.landmark]) * height - offset)
            x_max = min(width, max([lm.x for lm in hand_landmarks.landmark]) * width + offset)
            y_max = min(height, max([lm.y for lm in hand_landmarks.landmark]) * height + offset)

            # YOLO annotation values
            x_center = ((x_min + x_max) / 2) / width
            y_center = ((y_min + y_max) / 2) / height
            box_width = (x_max - x_min) / width
            box_height = (y_max - y_min) / height

            # Write annotation in YOLO format
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

    # Optional: Draw landmarks and bounding box for visualization
    mp_drawing = mp.solutions.drawing_utils
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

    # Save visualization
    visualized_path = os.path.join(output_dir, "visualized_" + os.path.basename(image_path))
    cv2.imwrite(visualized_path, image)
    print(f"Visualization saved: {visualized_path}")

    return True


def annotate_images(input_dir, output_dir, class_id):
    """Annotate all images in a single directory with YOLO-style annotations."""
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.8)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get all image files from the input directory
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Skipping invalid image: {image_path}")
            continue

        height, width = image.shape[:2]
        detect_and_annotate(image_path, output_dir, class_id, hands, width, height)

    hands.close()


if __name__ == "__main__":
    input_folder = "../Dataset/Imagesa"  # Path to folder containing images
    output_folder = "Datasetb/SPACE"  # Path to save annotations and visualizations
    gesture_class_id = 0  # Replace with the correct class ID

    # Annotate the images in the specified folder
    annotate_images(input_folder, output_folder, gesture_class_id)
