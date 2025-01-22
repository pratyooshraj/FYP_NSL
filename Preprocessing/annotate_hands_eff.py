import os
import cv2
import mediapipe as mp
from gesture_mapping import gesture_mapping_vowels, gesture_mapping_consonants


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
        hands_not_found_dir = os.path.join("../Dataset", "hands_not_found_cons_3_train")
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
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.8)

    for sub_dir in os.listdir(input_dir):
        sub_dir_path = os.path.join(input_dir, sub_dir)

        if not os.path.isdir(sub_dir_path):
            continue
        print(f"Annotating {sub_dir}")
        # class_id = gesture_mapping_vowels.get(sub_dir)
        class_id = gesture_mapping_consonants.get(sub_dir)
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
    src_dir = "../Dataset/YOLO_Data_prd_ver1_cons_3"
    dest_dir = "../Dataset/YOLO_Data_prd_ver1_cons_3"
    # Annotate training and testing data


    # remember to change folder for hands not found
    annotate_images(os.path.join(dest_dir, 'train', 'train_images'), os.path.join(dest_dir, 'train', 'train_annotations'))
    # annotate_images(os.path.join(dest_dir, 'test', 'test_images'), os.path.join(dest_dir, 'test', 'test_annotations'))
    # annotate_images(os.path.join(dest_dir, 'val', 'val_images'), os.path.join(dest_dir, 'val', 'val_annotations'))
    # test,val  done for ver1cons3 train remaining