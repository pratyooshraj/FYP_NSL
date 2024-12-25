import cv2
import mediapipe as mp
import os

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

    os.makedirs(output_dir, exist_ok=True)

    frame_count = 0
    print("Press 's' to save an image, 'q' to quit.")

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
            image_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved: {image_path}")
            frame_count += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    # hands.close()

# Example usage
output_dir = "captured_images"  # Directory to save images
capture_images(output_dir)