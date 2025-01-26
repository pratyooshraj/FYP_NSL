import os

def count_files_in_folders(folder_path, output_file="../Dataset/ver2_vowels.txt"):
    """
    Count the number of subfolders and files in each subfolder of the given folder.
    Append the results to a text file.

    Parameters:
        folder_path (str): Path to the main folder.
        output_file (str): Path to the output text file.
    """
    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist or is not a valid directory.")
        return

    # Initialize a counter for subfolders
    subfolder_count = 0
    result_lines = []

    # Walk through the subfolders
    for root, dirs, files in os.walk(folder_path):
        # Skip the main folder; process only its subfolders
        if root == folder_path:
            subfolder_count = len(dirs)  # Count subfolders in the main folder
            continue

        # Get the current subfolder name
        subfolder_name = os.path.basename(root)

        # Count all files in the current subfolder
        file_count = len(files)

        # Append the result for the current subfolder
        result_lines.append(f"Subfolder: {subfolder_name}, Files: {file_count}")

    # Add the summary
    result_lines.insert(0, f"Main Folder: {os.path.basename(folder_path)}, Subfolders: {subfolder_count}")

    # Write the results to the output file
    with open(output_file, "a") as file:
        file.write("\n".join(result_lines) + "\n")

    print(f"Results appended to '{output_file}'.")


# Example usage
# with open("../Dataset/aug_img_count.txt", "a") as file:
#     file.write("Captured Images" + "\n")
# folder_name = '../Dataset/augmented_images1/vowels'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/augmented_images1/consonants'
# count_files_in_folders(folder_name)
#
# with open("../Dataset/aug_img_count.txt", "a") as file:
#     file.write("\n\n\n"+"Video_to_img" + "\n")
# folder_name = '../Dataset/augmented_images2/NSL_Vowels'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/augmented_images2/NSL_Consonant_Part_1'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/augmented_images2/NSL_Consonant_Part_1_2'
# count_files_in_folders(folder_name)
#
# with open("../Dataset/aug_img_count.txt", "a") as file:
#     file.write("\n\n\n\n"+"combo" + "\n\n")
# folder_name = '../Dataset/augmented_images2/NSL_Consonant_combo'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/augmented_images2/NSL_Vowels_combo'
# count_files_in_folders(folder_name)

# with open("../Dataset/train_count_801010.txt", "a") as file:
#     file.write("\n\n\n\n"+"combo" + "\n\n")
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons/test/test_images'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons/train/train_images'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons/val/val_images'
# count_files_in_folders(folder_name)
#
# with open("../Dataset/train_count_801010.txt", "a") as file:
#     file.write("\n\n\n\n"+"combo" + "\n\n")
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons_2/test/test_images'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons_2/train/train_images'
# count_files_in_folders(folder_name)
# folder_name = '../Dataset/YOLO_Data_prd_ver1_cons_2/val/val_images'
# count_files_in_folders(folder_name)

with open("../Dataset/ver2_vowels.txt", "a") as file:
    file.write("all vowels" + "\n\n")
folder_name = '../Dataset/YOLO_vowels/train/images'
count_files_in_folders(folder_name)
folder_name = '../Dataset/YOLO_vowels/test/images'
count_files_in_folders(folder_name)
folder_name = '../Dataset/YOLO_vowels/val/images'
count_files_in_folders(folder_name)

