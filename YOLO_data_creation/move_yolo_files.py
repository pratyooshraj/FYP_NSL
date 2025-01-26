# to move images/annotations from sub-directory of letter to train/test/val folder
import os
import shutil

from gesture_mapping import gesture_mapping_vowels, gesture_mapping_consonants

def move_yolo_files(labels_dir):
    # Iterate through each subdirectory in the labels folder
    # for folder_name in gesture_mapping_vowels.keys():
    for folder_name in gesture_mapping_consonants.keys():
        folder_path = os.path.join(labels_dir, folder_name)
        if os.path.isdir(folder_path):
            # Move all files from the subdirectory to the main labels directory
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    shutil.move(file_path, labels_dir)
            # Remove the subdirectory if it's empty
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

    print("Files moved and empty subdirectories deleted successfully.")


dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/val/train_annotations'
move_yolo_files(dir_name)
dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/val/train_images'
move_yolo_files(dir_name)
# dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/train/train_annotations'
# move_yolo_files(dir_name)
# dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/train/train_images'
# move_yolo_files(dir_name)
# dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/val/val_annotations'
# move_yolo_files(dir_name)
# dir_name = '../Dataset/YOLO_Data_prd_ver1_cons/val/val_images'
# move_yolo_files(dir_name)