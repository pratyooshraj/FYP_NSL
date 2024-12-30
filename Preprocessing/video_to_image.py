# The script is used to convert videos in a directory to images of each letter. A folder of images for each letter is created.
# The video used here shows only single alphabet.
# Needs to be run 3 times (vowel, consonants_part1, consonants_part2)

import uuid
import cv2
import os

def resize_with_aspect_ratio(image, target_size=(640, 640)):
    """
    Resize an image to the target size while maintaining aspect ratio by cropping.

    Args:
        image (numpy.ndarray): Input image.
        target_size (tuple): Target size as (width, height).

    Returns:
        numpy.ndarray: Resized and cropped image.
    """
    target_width, target_height = target_size
    height, width = image.shape[:2]

    # Calculate the scaling factor
    scale = max(target_width / width, target_height / height)
    resized_width = int(width * scale)
    resized_height = int(height * scale)

    # Resize the image
    resized_image = cv2.resize(image, (resized_width, resized_height))

    # Crop the center
    start_x = (resized_width - target_width) // 2
    start_y = (resized_height - target_height) // 2
    cropped_image = resized_image[start_y:start_y + target_height, start_x:start_x + target_width]

    return cropped_image

def extract_frames(video_path, output_dir, video_name, frame_rate=10):
    """
    Extracts frames from a video and saves them to a directory.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save the extracted frames.
        video_name (str): Name of the video, used in the frame filenames.
        frame_rate (int): Number of frames to extract per second of video.
    """
    if "_" in video_name:
        video_name = video_name.split("_", 1)[1]

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Capture the video
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # Get video properties
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"Processing '{video_path}'")
    print(f" - Total Frames: {total_frames}")
    print(f" - FPS: {fps}")
    print(f" - Duration: {duration:.2f} seconds")

    # Calculate the interval between frames to save
    interval = int(fps / frame_rate)
    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Save every 'interval' frame
        if frame_count % interval == 0:
            unique_id = uuid.uuid4()  # Generate a unique identifier
            frame_filename = os.path.join(output_dir, f"{video_name}_{unique_id}_{saved_frame_count:04d}.jpg")
            frame = cv2.resize(frame, (640, 640))           # check before saving
            # frame = resize_with_aspect_ratio(frame, target_size=(640, 640))
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

    video_capture.release()
    print(f"Frames saved to {output_dir}: {saved_frame_count} frames extracted")

def process_videos(input_dir, output_dir, frame_rate=10):
    """
    Processes all videos in a directory, extracting frames for each video.

    Args:
        input_dir (str): Directory containing video files.
        output_dir (str): Directory to save all extracted frames.
        frame_rate (int): Number of frames to extract per second of video.
    """
    # Get a list of all video files in the input directory
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]

    if not video_files:
        print("No video files found in the input directory.")
        return

    print(f"Found {len(video_files)} video(s) in {input_dir}")

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        video_name = os.path.splitext(video_file)[0]

        # Create a specific output folder for this video's frames
        video_output_dir = os.path.join(output_dir, video_name)

        # Extract frames for the current video
        extract_frames(video_path, video_output_dir, video_name, frame_rate)

# if __name__ == "__main__":
# Example usage
#     input_dir = "Dataset/Videos/NSL_Vowel/S2_NSL_Vowel_Unprepared_Dark_Cropped"
#     output_dir = "Dataset/Images/NSL_Vowel/S2_NSL_Vowel_Unprepared_Dark_Cropped"
#     frame_rate = 15  # Extract 15 frames per second
#
#     process_videos(input_dir, output_dir, frame_rate)

if __name__ == "__main__":
    # Parent directory containing subdirectories of videos

    # part 1
    # parent_dir = "../Dataset/Videos/NSL_Vowel"
    # output_parent_dir = "../Dataset/Images_20fr/NSL_Vowel"

    # part 2
    # parent_dir = "../Dataset/Videos/NSL_Consonant_Part_1"
    # output_parent_dir = "../Dataset/Images_20fr/NSL_Consonant_Part_1"

    # part 3
    parent_dir = "../Dataset/Videos/NSL_Consonant_Part_1_2"
    output_parent_dir = "../Dataset/Images_20fr/NSL_Consonant_Part_1_2"

    frame_rate = 20  # Extract 20 frames per second

    # Loop through each subdirectory in the parent directory
    for sub_dir in os.listdir(parent_dir):
        sub_dir_path = os.path.join(parent_dir, sub_dir)

        # Check if it's a directory
        if os.path.isdir(sub_dir_path):
            print(f"Processing videos in subdirectory: {sub_dir}")

            # Define the corresponding output subdirectory
            output_sub_dir = os.path.join(output_parent_dir, sub_dir)
            # print(f"output_sub_dir={output_sub_dir}")
            # print(f"sub_dir_path={sub_dir_path}")
            # Process videos in the current subdirectory
            process_videos(sub_dir_path, output_sub_dir, frame_rate)
