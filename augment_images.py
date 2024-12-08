# augment_images.py

import cv2
import numpy as np
import random
import os


def random_rotate(image, angle_range=(-15, 15)):
    """Randomly rotate the image."""
    height, width = image.shape[:2]
    angle = random.uniform(*angle_range)
    matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
    return cv2.warpAffine(image, matrix, (width, height), borderMode=cv2.BORDER_REFLECT)


def adjust_brightness_contrast(image, brightness_range=(0.8, 1.2), contrast_range=(0.8, 1.2)):
    """Adjust brightness and contrast of the image."""
    brightness = random.uniform(*brightness_range)
    contrast = random.uniform(*contrast_range)
    return cv2.convertScaleAbs(image, alpha=contrast, beta=int(brightness * 50))


def random_scale(image, scale_range=(0.8, 1.2)):
    """Randomly scale the image."""
    height, width = image.shape[:2]
    scale = random.uniform(*scale_range)
    new_width = int(width * scale)
    new_height = int(height * scale)
    scaled_image = cv2.resize(image, (new_width, new_height))

    if scale > 1:
        start_x = (new_width - width) // 2
        start_y = (new_height - height) // 2
        return scaled_image[start_y:start_y + height, start_x:start_x + width]
    else:
        pad_x = (width - new_width) // 2
        pad_y = (height - new_height) // 2
        return cv2.copyMakeBorder(scaled_image, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)


def random_crop(image, crop_fraction=0.1):
    """Randomly crop the image."""
    height, width = image.shape[:2]
    max_crop_x = int(width * crop_fraction)
    max_crop_y = int(height * crop_fraction)

    crop_x = random.randint(0, max_crop_x)
    crop_y = random.randint(0, max_crop_y)

    return image[crop_y:height - crop_y, crop_x:width - crop_x]


def augment_image(image):
    """Apply all augmentations to the image."""
    image = random_rotate(image)
    image = adjust_brightness_contrast(image)
    image = random_scale(image)
    image = random_crop(image)
    return image


def augment_images(input_dir, output_dir):
    """Apply augmentation to all images in the input directory."""
    for root, _, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        save_dir = os.path.join(output_dir, relative_path)
        os.makedirs(save_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                file_path = os.path.join(root, file)
                image = cv2.imread(file_path)

                if image is None:
                    print(f"Error loading {file_path}")
                    continue

                augmented_image = augment_image(image)

                # Save the augmented image
                save_path = os.path.join(save_dir, f"aug_{file}")
                cv2.imwrite(save_path, augmented_image)
                print(f"Processed and saved: {save_path}")


if __name__ == "__main__":
    # Example usage
    input_dir = "path_to_extracted_frames"
    output_dir = "path_to_augmented_images"
    augment_images(input_dir, output_dir)
