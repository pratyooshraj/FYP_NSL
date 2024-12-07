import uuid
import cv2
import os

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

# Example usage
input_dir = "Dataset/Videos/NSL_Vowel/S1_NSL_Vowel_Unprepared_Bright"
output_dir = "Dataset/Images/NSL_Vowel/S1_NSL_Vowel_Unprepared_Bright"
frame_rate = 15  # Extract 15 frames per second

process_videos(input_dir, output_dir, frame_rate)
