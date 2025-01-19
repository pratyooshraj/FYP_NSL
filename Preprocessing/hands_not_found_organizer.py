import os
import shutil

from gesture_mapping import gesture_mapping_vowels, gesture_mapping_consonants

# Combine all keys from both dictionaries
prefixes = set(gesture_mapping_vowels.keys()).union(gesture_mapping_consonants.keys())

# Path to the directory containing the files
base_dir = 'hands_not_found'

# Ensure each prefix has a corresponding subdirectory
for prefix in prefixes:
    sub_dir = os.path.join(base_dir, prefix)
    os.makedirs(sub_dir, exist_ok=True)

# Move files to their respective subdirectories
for file_name in os.listdir(base_dir):
    if file_name.endswith('.jpg'):  # Check for .jpg files
        for prefix in prefixes:
            if file_name.startswith(prefix + '_'):
                source_path = os.path.join(base_dir, file_name)
                destination_path = os.path.join(base_dir, prefix, file_name)
                shutil.move(source_path, destination_path)
                break

print("Files have been organized into their respective subdirectories.")
