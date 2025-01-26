import os
from gesture_mapping import gesture_mapping_consonants, gesture_mapping_vowels


def delete_files_with_suffix(folder_path, suffixes, extensions):
    """
    Deletes files with the specified suffixes and extensions in the given folder.

    Args:
        folder_path (str): Path to the folder where files should be deleted.
        suffixes (list): List of suffixes to look for (e.g., ['_sc', '_rot']).
        extensions (list): List of file extensions to look for (e.g., ['.jpg', '.txt']).

    Returns:
        int: Total number of files deleted.
    """
    total_deleted = 0

    for filename in os.listdir(folder_path):
        # Check if the file has any of the specified suffixes and extensions
        if any(filename.endswith(suffix + ext) for suffix in suffixes for ext in extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                os.remove(file_path)
                total_deleted += 1
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    return total_deleted

# Define suffixes and extensions to target
suffixes_to_delete = ["_sc", "_rot"]
images_extensions = [".png", ".jpg"]
annotations_extensions = [".txt"]

# letters = list(gesture_mapping_vowels.keys())
letters = list(gesture_mapping_consonants.keys())
total=0
for letter in letters:
    print(f"Folder for {letter}...")

# Define folder paths
    images_folder = f"../Dataset/YOLO_Data_prd_ver1_cons_3/test/test_images/{letter}"
    annotations_folder = f"../Dataset/YOLO_Data_prd_ver1_cons_3/test/test_annotations/{letter}"

    # Delete files and calculate totals
    images_deleted = 0
    annotations_deleted = 0

    if os.path.exists(images_folder):
        images_deleted = delete_files_with_suffix(images_folder, suffixes_to_delete, images_extensions)
        print(f"Total files deleted in 'images' folder: {images_deleted}")
    else:
        print("The 'images' folder does not exist.")

    if os.path.exists(annotations_folder):
        annotations_deleted = delete_files_with_suffix(annotations_folder, suffixes_to_delete, annotations_extensions)
        print(f"Total files deleted in 'annotations' folder: {annotations_deleted}")
    else:
        print("The 'annotations' folder does not exist.")

    # Print separate counts
    # print(
    #     f"Summary:\n - Images folder: {images_deleted} files deleted\n - Annotations folder: {annotations_deleted} files deleted")
    total+=images_deleted

print(total)