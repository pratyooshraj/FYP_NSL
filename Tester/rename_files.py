import os


def rename_files_in_folder(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return
        count=0
        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            # Check if the filename starts with 'RE_'
            count+=1
            if filename.startswith("RE_"):
                # Create the new filename
                new_filename = "RI_" + filename[3:]

                # Get full paths for renaming
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"Skipped: {filename}")

        print("Renaming completed.")
        print(f"{count} files renamed.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
folder_path = "../Dataset/Images_20fr/NSL_Vowel/S2_NSL_Vowel_Unprepared_Dark_Cropped/S2_RE"  # Replace with your folder path
rename_files_in_folder(folder_path)
