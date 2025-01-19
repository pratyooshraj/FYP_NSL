import shutil
import mediapipe as mp
import cv2
import numpy as np
import random
import os

from gesture_mapping import gesture_mapping_consonants, gesture_mapping_vowels


def random_rotate(image, angle_range=(-25, 25)):
    """Randomly rotate the image."""
    height, width = image.shape[:2]
    angle = random.uniform(*angle_range)
    matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
    return cv2.warpAffine(image, matrix, (width, height), borderMode=cv2.BORDER_REFLECT)


def adjust_brightness_contrast(image, brightness_range=(0.75, 1.25), contrast_range=(0.8, 1.2)):
    """Adjust brightness and contrast of the image."""
    brightness = random.uniform(*brightness_range)
    contrast = random.uniform(*contrast_range)
    return cv2.convertScaleAbs(image, alpha=contrast, beta=int(brightness * 50))


def random_scale(image, scale_range=(0.65, 1.35)):
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


def add_gaussian_blur(image, blur_limit=(1, 4)):
    """Apply Gaussian blur to the image."""
    kernel_size = random.choice(range(blur_limit[0], blur_limit[1] + 1, 2))  # Kernel size must be odd
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def change_background_color(image, color_range=((0, 0, 0), (255, 255, 255))):
    """Change background color randomly."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a binary mask: Background pixels = 255, Foreground pixels = 0
    _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # Invert the mask: Background pixels = 0, Foreground pixels = 255
    inverted_mask = cv2.bitwise_not(mask)

    # Generate a random background color
    background_color = tuple(random.randint(low, high) for low, high in zip(color_range[0], color_range[1]))

    # Create a solid color background image
    background = np.full_like(image, background_color)

    # Combine the original foreground with the new background
    foreground = cv2.bitwise_and(image, image, mask=mask)  # Retain only the foreground
    updated_background = cv2.bitwise_and(background, background, mask=inverted_mask)  # Apply the new background

    # Merge the foreground and the new background
    final_image = cv2.add(foreground, updated_background)

    return final_image


def change_background_with_mediapipe(image, mp_selfie_segmentation, color_range=((0, 0, 0), (255, 255, 255))):
    """
    Change the background color of an image using Mediapipe Selfie Segmentation with random translucency.

    Parameters:
        image (numpy.ndarray): Input image (BGR).
        mp_selfie_segmentation (module): Mediapipe Selfie Segmentation module.
        color_range (tuple): Range of colors for random background ((low_B, low_G, low_R), (high_B, high_G, high_R)).

    Returns:
        numpy.ndarray: Image with the updated translucent background.
    """
    # Initialize Mediapipe Selfie Segmentation
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as segmenter:
        # Convert the image to RGB (required by Mediapipe)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Generate the segmentation mask
        results = segmenter.process(rgb_image)
        mask = results.segmentation_mask

        # Threshold the mask to create a binary foreground-background mask
        binary_mask = (mask > 0.5).astype(np.uint8) * 255  # Foreground = 255, Background = 0

        # Generate a random background color

        background_color = tuple(random.randint(low, high) for low, high in zip(color_range[0], color_range[1]))
        solid_background = np.full_like(image, background_color)

        # Generate a random alpha value between 0.5 and 0.7 for translucency
        alpha = random.uniform(0.5, 0.7)

        # Apply translucency to the background
        translucent_background = cv2.addWeighted(solid_background, alpha, image, 1 - alpha, 0)

        # Apply the masks to combine the foreground with the new background
        foreground = cv2.bitwise_and(image, image, mask=binary_mask)  # Keep the person
        inverted_mask = cv2.bitwise_not(binary_mask)  # Invert the mask
        updated_background = cv2.bitwise_and(translucent_background, translucent_background, mask=inverted_mask)  # New background

        # Combine the foreground and the new translucent background
        final_image = cv2.add(foreground, updated_background)
        return final_image


def augment_image(image):
    """Apply all augmentations to the image."""
    image = random_rotate(image)
    image = change_background_color(image)
    image = adjust_brightness_contrast(image)
    image = random_scale(image)
    image = add_gaussian_blur(image)
    return image


def augment_images(input_dir, output_dir):
    """Apply augmentation to all images in the input directory."""
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
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

                original_save_path = os.path.join(save_dir, file)
                shutil.copy(file_path, original_save_path)
                print(f"Original image copied to: {original_save_path}")

                augmented_image = augment_image(image)
                rot_image=random_rotate(image)
                scale_image=random_scale(image)
                # bright_image=adjust_brightness_contrast(image)
                # blur_image = add_gaussian_blur(image)
                bg_changed_image = change_background_with_mediapipe(image,mp_selfie_segmentation)

                # Save the augmented images
                file_name, file_ext = os.path.splitext(file)
                augmented_file_name = f"{file_name}_aug{file_ext}"
                # blur_file_name = f"{file_name}_blur{file_ext}"
                bg_changed_file_name = f"{file_name}_bg{file_ext}"
                rot_file_name = f"{file_name}_rot{file_ext}"
                scale_file_name = f"{file_name}_sc{file_ext}"
                # bright_file_name = f"{file_name}_br{file_ext}"

                # Construct the save paths
                save_path = os.path.join(save_dir, augmented_file_name)
                # blur_save_path = os.path.join(save_dir, blur_file_name)
                bg_save_path = os.path.join(save_dir, bg_changed_file_name)
                rot_save_path = os.path.join(save_dir, rot_file_name)
                scale_save_path = os.path.join(save_dir, scale_file_name)
                # br_save_path = os.path.join(save_dir, bright_file_name)

                cv2.imwrite(save_path, augmented_image)
                # cv2.imwrite(blur_save_path, blur_image)
                cv2.imwrite(bg_save_path, bg_changed_image)
                cv2.imwrite(rot_save_path, rot_image)
                cv2.imwrite(scale_save_path, scale_image)
                # cv2.imwrite(br_save_path, bright_image)
                print(f"Processed and saved: {save_path}")


if __name__ == "__main__":
    # Example usage
    letters = list(gesture_mapping_vowels.keys())
    # letters = list(gesture_mapping_consonants.keys())

    for letter in letters:
        print(f"Folder for {letter}...")
        input_dir = f"../Dataset/Images_20_final/NSL_Vowels_combo/{letter}"
        output_dir = f"../Dataset/augmented_images2/NSL_Vowels_combo/{letter}"
        augment_images(input_dir, output_dir)
