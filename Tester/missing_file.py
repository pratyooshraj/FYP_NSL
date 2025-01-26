import os


def find_missing_files(folder1, folder2, ext1, ext2):
    """
    Finds and prints the names of files missing in each folder.

    Args:
        folder1 (str): Path to the first folder.
        folder2 (str): Path to the second folder.
        ext1 (str): File extension for files in the first folder (e.g., '.jpg').
        ext2 (str): File extension for files in the second folder (e.g., '.txt').
    """
    # Get the base names of files without extensions in each folder
    files1 = {os.path.splitext(f)[0] for f in os.listdir(folder1) if f.endswith(ext1)}
    files2 = {os.path.splitext(f)[0] for f in os.listdir(folder2) if f.endswith(ext2)}

    # Determine missing files
    missing_in_folder1 = files2 - files1
    missing_in_folder2 = files1 - files2

    # Print results
    if missing_in_folder1:
        print(f"Files missing in '{folder1}' (expected {ext1}): {', '.join(missing_in_folder1)}")
    else:
        print(f"No files are missing in '{folder1}'.")

    if missing_in_folder2:
        print(f"Files missing in '{folder2}' (expected {ext2}): {', '.join(missing_in_folder2)}")
    else:
        print(f"No files are missing in '{folder2}'.")


# Example usage
letters = ['TAA','MA','HA','TRA']
total=0
for letter in letters:
    print(f"Folder for {letter}...")
    images_folder = f"../Dataset/YOLO_Data_prd_ver1_cons/val/val_images/{letter}"
    annotations_folder = f"../Dataset/YOLO_Data_prd_ver1_cons/val/val_annotations/{letter}"

    # Ensure both folders exist
    if os.path.exists(images_folder) and os.path.exists(annotations_folder):
        find_missing_files(images_folder, annotations_folder, ".jpg", ".txt")
    else:
        print("Both folders must exist to check for missing files.")
