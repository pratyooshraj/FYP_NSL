import os
import shutil
from sklearn.model_selection import train_test_split

def split_val_to_val_test(val_image_dir, val_annotation_dir, test_image_dir, test_annotation_dir, annotation_extension=".txt"):
    """
    Split the current `val` images and annotations into separate `val` and `test` folders.
    Ensures that images and their corresponding annotations are moved together.
    """
    if not os.path.exists(val_image_dir) or not os.path.exists(val_annotation_dir):
        raise FileNotFoundError(f"Validation directories {val_image_dir} or {val_annotation_dir} do not exist.")

    # Ensure test directories exist
    os.makedirs(test_image_dir, exist_ok=True)
    os.makedirs(test_annotation_dir, exist_ok=True)

    # Loop through each class folder in `val_image_dir`
    for class_folder in os.listdir(val_image_dir):
        class_val_image_path = os.path.join(val_image_dir, class_folder)
        class_val_annotation_path = os.path.join(val_annotation_dir, class_folder)
        class_test_image_path = os.path.join(test_image_dir, class_folder)
        class_test_annotation_path = os.path.join(test_annotation_dir, class_folder)

        if not os.path.isdir(class_val_image_path):
            continue

        # Ensure test class folders exist
        os.makedirs(class_test_image_path, exist_ok=True)
        os.makedirs(class_test_annotation_path, exist_ok=True)

        # Get list of image files in the class folder
        image_files = [f for f in os.listdir(class_val_image_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # Split image files into 50% val and 50% test
        val_files, test_files = train_test_split(image_files, test_size=0.1, random_state=42)

        # Move images and corresponding annotation files
        for file_set, (image_dest, annotation_dest) in [
            (test_files, (class_test_image_path, class_test_annotation_path)),
            (val_files, (class_val_image_path, class_val_annotation_path)),
        ]:
            for file_name in file_set:
                # Image paths
                src_image_path = os.path.join(class_val_image_path, file_name)
                dst_image_path = os.path.join(image_dest, file_name)

                # Annotation paths
                annotation_file = os.path.splitext(file_name)[0] + annotation_extension
                src_annotation_path = os.path.join(class_val_annotation_path, annotation_file)
                dst_annotation_path = os.path.join(annotation_dest, annotation_file)

                # Move image
                shutil.move(src_image_path, dst_image_path)

                # Move annotation (if it exists)
                if os.path.exists(src_annotation_path):
                    shutil.move(src_annotation_path, dst_annotation_path)

        print(f"Split completed for class: {class_folder}")

# Example usage
# val_image_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train/train_images"  # Path to val images
# val_annotation_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train/train_annotations"  # Path to val annotations
# test_image_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train1/train_images"  # Path to test images
# test_annotation_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train1/train_annotations"  # Path to test annotations

val_image_directory = "../Dataset/YOLO_Data_prd_ver1_cons/train1/train_images"  # Path to val images
val_annotation_directory = "../Dataset/YOLO_Data_prd_ver1_cons/train1/train_annotations"  # Path to val annotations
test_image_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train111/test11_images"  # Path to test images
test_annotation_directory = "../Dataset/YOLO_Data_prd_ver1_cons_2/train111/test11_annotations"  # Path to test annotations

split_val_to_val_test(val_image_directory, val_annotation_directory, test_image_directory, test_annotation_directory)


