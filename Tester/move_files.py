import os
import shutil
from gesture_mapping import gesture_mapping_consonants, gesture_mapping_vowels


def move_files(source_dir, destination_dir):
    """
    Moves all files from source_dir to destination_dir without overwriting existing files.

    Args:
        source_dir (str): Path to the source directory.
        destination_dir (str): Path to the destination directory.
    Returns:
        int: Number of files moved.
    """
    files_moved = 0
    try:
        if not os.path.exists(source_dir):
            print(f"Source directory does not exist: {source_dir}")
            return files_moved

        # Ensure destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # List all files in the source directory
        files = os.listdir(source_dir)

        for file_name in files:
            source_file = os.path.join(source_dir, file_name)
            destination_file = os.path.join(destination_dir, file_name)

            # Check if the file already exists in the destination
            if os.path.isfile(source_file):
                if os.path.exists(destination_file):
                    # Rename the file to avoid overwriting
                    base, extension = os.path.splitext(file_name)
                    count = 1
                    new_file_name = f"{base}_{count}{extension}"
                    new_destination_file = os.path.join(destination_dir, new_file_name)
                    while os.path.exists(new_destination_file):
                        count += 1
                        new_file_name = f"{base}_{count}{extension}"
                        new_destination_file = os.path.join(destination_dir, new_file_name)
                    destination_file = new_destination_file
                    print(f"File {file_name} already exists. Renamed to {new_file_name}")

                # Move the file
                shutil.move(source_file, destination_file)
                files_moved += 1

        print(f"Files moved from {source_dir} to {destination_dir}: {files_moved}")
        return files_moved

    except Exception as e:
        print(f"Error while moving files: {e}")
        return files_moved


# Example usage
letters = list(gesture_mapping_consonants.keys())
total = 0

for letter in letters:
    print(f"Moving {letter}...")
    source = f"../Dataset/YOLO_Data_prd_ver1_cons_3/test/test_images/{letter}"
    destination = f"../Dataset/YOLO_Data_prd_ver1_cons_3/val/val_images/{letter}"

    total += move_files(source, destination)

print(f"Total files moved = {total}")
