import os
import shutil

data_folder = 'Dataset/YOLO_Data_ver4'  # Replace with your folder path

# Check if the main data folder exists
if os.path.exists(data_folder) and os.path.isdir(data_folder):
    for root_dir in os.listdir(data_folder):
        root_dir_path = os.path.join(data_folder, root_dir)

        # Ensure the root_dir_path is a directory
        if os.path.isdir(root_dir_path):
            for sub_dir in os.listdir(root_dir_path):
                sub_dir_path = os.path.join(root_dir_path, sub_dir)

                # Ensure the sub_dir_path is a directory
                if os.path.isdir(sub_dir_path):
                    for nested_dir in os.listdir(sub_dir_path):
                        nested_dir_path = os.path.join(sub_dir_path, nested_dir)

                        # Ensure the nested_dir_path is a directory
                        if os.path.isdir(nested_dir_path):
                            for file in os.listdir(nested_dir_path):
                                file_path = os.path.join(nested_dir_path, file)

                                # Check if it's a file and move it to the parent directory
                                if os.path.isfile(file_path):
                                    shutil.move(file_path, sub_dir_path)

                            # Remove the empty nested directory
                            os.rmdir(nested_dir_path)

    print("All images moved to the respective main folders.")
else:
    print(f"Error: The folder '{data_folder}' does not exist or is not a directory.")
