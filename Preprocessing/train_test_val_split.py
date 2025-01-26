import os
from sklearn.model_selection import train_test_split
import shutil

def split_data(src_dir, dest_dir, train_size=0.8, val_size=0.1, test_size=0.1):
    """Split the dataset into train, validation, and test sets, maintaining class structure."""

    # Validate that the sum of train_size, val_size, and test_size is 1
    if not abs((train_size + val_size + test_size) - 1.0) < 1e-9:
        print(train_size + val_size + test_size)
        raise ValueError("The sum of train_size, val_size, and test_size must equal 1.0")

    # Create directories for train, validation, and test sets
    train_dir = os.path.join(dest_dir, 'train', 'train_images')
    val_dir = os.path.join(dest_dir, 'val', 'val_images')
    test_dir = os.path.join(dest_dir, 'test', 'test_images')

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Loop through each class folder in the source directory
    for sub_dir in os.listdir(src_dir):
        print(f"split for {sub_dir}")
        sub_dir_path = os.path.join(src_dir, sub_dir)

        if not os.path.isdir(sub_dir_path):
            continue

        # Get list of image files in the current class folder
        image_files = [f for f in os.listdir(sub_dir_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # Split data into train and remaining (val + test) set
        train_files, remaining_files = train_test_split(image_files, train_size=train_size, random_state=42)

        # Split remaining files into validation and test sets
        val_files, test_files = train_test_split(remaining_files, train_size=val_size / (val_size + test_size),random_state=42)

        # Copy files into corresponding directories
        for file_set, save_dir in [(train_files, train_dir), (val_files, val_dir), (test_files, test_dir)]:
            class_save_dir = os.path.join(save_dir, sub_dir)
            os.makedirs(class_save_dir, exist_ok=True)
            for file in file_set:
                shutil.copy(os.path.join(sub_dir_path, file), os.path.join(class_save_dir, file))



if __name__ == "__main__":
    # src_dir = "../Dataset/augmented_images1/vowels"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1"
    # # Split the data
    # split_data(src_dir, dest_dir,0.8,0.1,0.1)
    # print("captured vowel split done")
    #
    # src_dir = "../Dataset/augmented_images2/NSL_Vowels_combo"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1"
    # # Split the data
    # split_data(src_dir, dest_dir, 0.8, 0.1, 0.1)
    # print("combo vowel split done")

    # src_dir = "../Dataset/augmented_images2/NSL_Vowels"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1"
    # # Split the data
    # split_data(src_dir, dest_dir, 0.7, 0.2, 0.1)
    # print("vowel split done")

    # src_dir = "../Dataset/augmented_images1/consonants"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1_cons"
    # # Split the data
    # split_data(src_dir, dest_dir,0.8,0.1,0.1)
    # print("captured consonant split done")
    #
    # src_dir = "../Dataset/augmented_images2/NSL_Consonant_combo"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1_cons"
    # # Split the data
    # split_data(src_dir, dest_dir, 0.8, 0.1, 0.1)
    # print("combo consonant split done")

    # src_dir = "../Dataset/augmented_images2/NSL_Consonant_Part_1"
    # dest_dir = "../Dataset/YOLO_Data_prd_ver1_cons_2"
    # # Split the data
    # split_data(src_dir, dest_dir, 0.65, 0.2, 0.15)
    # print("cons1 split done")

    src_dir = "../Dataset/augmented_images2/NSL_Consonant_Part_1_2"
    dest_dir = "../Dataset/YOLO_Data_prd_ver1_cons_3"
    # Split the data
    split_data(src_dir, dest_dir, 0.8, 0.1, 0.1)
    print("cons2 split done")

