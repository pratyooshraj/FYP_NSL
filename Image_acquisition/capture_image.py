import cv2
import mediapipe as mp
import os

from gesture_mapping import gesture_mapping_vowels, gesture_mapping_consonants

def capture_images(output_dir, save_images=True):
    """
    Captures images from a webcam, detects hand landmarks in real-time using MediaPipe,
    and optionally saves the frames with detected hands.

    Args:
        output_dir (str): Directory to save captured images.
        save_images (bool): Whether to save the images with detected hands.
    """
    # # Initialize MediaPipe Hands
    # mp_hands = mp.solutions.hands
    # hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5)
    #
    # mp_drawing = mp.solutions.drawing_utils

    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return
    # gesture_keys = list(gesture_mapping_vowels.keys())
    gesture_keys = list(gesture_mapping_consonants.keys())
    count_letter=-1
    letter_dir=os.path.join(output_dir,gesture_keys[count_letter])
    os.makedirs(letter_dir, exist_ok=True)

    frame_count = 0
    print("Press 's' to save an image, 'q' to quit, 'n' to move to next letter.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read a frame from the webcam.")
            break

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB (MediaPipe requires RGB images)
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #
        # # Process the frame for hand detection
        # results = hands.process(frame_rgb)
        #
        # # Draw hand landmarks on the frame
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame
        cv2.imshow("Hand Landmark Detection", frame)

        # Handle user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit
            print("Quitting...")
            break
        elif key == ord('s') and save_images:  # Save image
            image_path = os.path.join(letter_dir, f"{gesture_keys[count_letter]}_blue_frame_{frame_count:04d}.jpg")
            cv2.imwrite(image_path, cv2.flip(frame, 1))
            print(f"Image saved: {image_path}")
            frame_count += 1
        elif key == ord('n'):  # Move to next gesture
            count_letter += 1
            if count_letter < len(gesture_keys):
                print(f"Current letter: {gesture_keys[count_letter]}")
                letter_dir = os.path.join(output_dir, gesture_keys[count_letter])
                os.makedirs(letter_dir, exist_ok=True)
                frame_count = 0  # Reset frame count for the new gesture
            else:
                print("All gestures captured!")
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    # hands.close()

# Example usage
# change frame number to prevent overwriting of images
output_dir = "../Dataset"  # Directory to save images
# output_dir = "../Dataset/captured_images/consonants"  # Directory to save images
capture_images(output_dir)
