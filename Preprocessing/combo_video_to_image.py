import cv2
import os
import uuid
# import pygame
import time
# from moviepy import VideoFileClip
from gesture_mapping import gesture_mapping_vowels

# Extract the keys (gesture names) from the dictionary
gesture_sequence = list(gesture_mapping_vowels.keys())

# Path to save the captured images
output_folder = 'captured_images'
os.makedirs(output_folder, exist_ok=True)

# Load the video
video_path = '../Dataset/Videos/NSL_Vowel_combo/S3_NSL_Vowel_Prepared/S3_NSL_Vowel_Prepared_Camera_all.mov'  # Update with the actual path to your video file

# # Use moviepy to extract audio from the video
# clip = VideoFileClip(video_path)
# audio_path = '../extracted_audio.wav'
# clip.audio.write_audiofile(audio_path)  # Extract and save audio as WAV file
#
# # Initialize pygame for audio playback
# pygame.mixer.init()
#
# # Load and play the extracted audio
# pygame.mixer.music.load(audio_path)
# pygame.mixer.music.play(-1, 0.0)  # Loop the sound

# Load the video for frame-by-frame processing
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("Error: Cannot open video.")

# Get the total number of frames and frames per second (fps) of the video
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# To keep track of the current gesture index
gesture_index = 0

# Get the duration of the video
# video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps  # Duration in seconds
# # video_duration = clip.duration  # Duration in seconds
# start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading the video.")
        break

    # Display the current frame
    cv2.imshow('Video', frame)

    # Adjust the delay to match the video's frame rate
    key = cv2.waitKey(int(1000 / fps)) & 0xFF

    # Capture image when spacebar is pressed
    if key == ord(' '):  # Spacebar key to capture image
        if gesture_index < len(gesture_sequence):
            # Get the current gesture from the sequence
            gesture = gesture_sequence[gesture_index]

            # Generate a unique UUID for the image filename
            unique_id = uuid.uuid4().hex  # Generate a unique ID
            filename = f"{gesture}_{unique_id}.jpg"
            file_path = os.path.join(output_folder, filename)

            # Save the captured frame as an image
            cv2.imwrite(file_path, frame)
            print(f"Captured image saved as {file_path}")

            # Move to the next gesture in the sequence
            gesture_index += 1
        else:
            print("All gestures have been captured.")
            break  # Stop if all gestures have been captured

    # Press 'q' to exit the video
    if key == ord('q'):
        print("Video playback terminated by user.")
        break

    # # If the video is finished, break the loop
    # elapsed_time = time.time() - start_time
    # if elapsed_time >= video_duration:
    #     break

# Stop the audio and release resources
# pygame.mixer.music.stop()
cap.release()
cv2.destroyAllWindows()
