import cv2
import os
import uuid
# import pygame
import time
# from moviepy import VideoFileClip
from gesture_mapping import gesture_mapping_vowels, gesture_mapping_consonants

# Path to save the captured images
output_dir = '../Dataset/Images_20fr/NSL_Consonant_combo'
os.makedirs(output_dir, exist_ok=True)
# Load the video
video_path = '../Dataset/Videos/NSL_Consonant_combo/S14_NSL_Consonant_RealWorld/S14_NSL_Consonant.mov'  # Update with the actual path to your video file

# # Use moviepy to extract audio from the videos
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

# gesture_keys = list(gesture_mapping_vowels.keys())
gesture_keys = list(gesture_mapping_consonants.keys())
count_letter=0
letter_dir=os.path.join(output_dir,gesture_keys[count_letter])
os.makedirs(letter_dir, exist_ok=True)

# Get the duration of the video
# video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps  # Duration in seconds
# # video_duration = clip.duration  # Duration in seconds
# start_time = time.time()
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# Maximize the window
cv2.resizeWindow('Video', 720, 640)
# cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading the video.")
        break

    # Display the current frame
    cv2.imshow('Video', frame)

    key = cv2.waitKey(int(1000 / fps )) & 0xFF

    # Capture image when spacebar is pressed
    if key == ord('s'):
        if count_letter < len(gesture_keys):
            unique_id = uuid.uuid4().hex  # Generate a unique ID
            filename = f"{gesture_keys[count_letter]}_{unique_id}.jpg"
            file_path = os.path.join(letter_dir, filename)

            # Save the captured frame as an image
            cv2.imwrite(file_path, frame)
            print(f"{file_path} saved")

        else:
            print("All gestures have been captured.")
            break  # Stop if all gestures have been captured
    elif key==ord('n'):
        count_letter+=1
        if count_letter < len(gesture_keys):
            letter_dir = os.path.join(output_dir, gesture_keys[count_letter])
            os.makedirs(letter_dir, exist_ok=True)
            unique_id = uuid.uuid4().hex  # Generate a unique ID
            filename = f"{gesture_keys[count_letter]}_{unique_id}.jpg"
            file_path = os.path.join(letter_dir, filename)

            # Save the captured frame as an image
            cv2.imwrite(file_path, frame)
            print(f"{file_path} saved")
        else:
            print("All gestures have been captured.")
            break
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
