import os
import re

# Mapping of gestures to new indices (0-based)
gesture_mapping_consonants = {
    'KA': 13, 'KHA': 14, 'GA': 15, 'GHA': 16, 'NGA': 17, 'CHA': 18, 'CHHA': 19, 'JA': 20,
    'JHA': 21, 'YAN': 22, 'TA': 23, 'THA': 24, 'DA': 25, 'DHA': 26, 'NA': 27, 'TAA': 28,
    'THAA': 29, 'DAA': 30, 'DHAA': 31, 'NAA': 32, 'PA': 33, 'PHA': 34, 'BA': 35, 'BHA': 36,
    'MA': 37, 'YA': 38, 'RA': 39, 'LA': 40, 'WA': 41, 'T_SHA': 42, 'M_SHA': 43, 'D_SHA': 44,
    'HA': 45, 'KSHA': 46, 'TRA': 47, 'GYA': 48, 'SPACE': 49
}

# Generate the mapping for reindexing
new_mapping = {gesture: new_index for new_index, (gesture, _) in
               enumerate(sorted(gesture_mapping_consonants.items(), key=lambda x: x[1]))}

# Directory containing the label `.txt` files
labels_dir = "../Dataset/YOLO_consonants/train/labels"
index=0
# Process each `.txt` file in the directory
for filename in os.listdir(labels_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(labels_dir, filename)
        index+=1

        # Read the contents of the file
        with open(filepath, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                old_class_id = int(parts[0])

                # Find the gesture name based on the filename
                for gesture, old_index in gesture_mapping_consonants.items():
                    if old_index == old_class_id:
                        new_class_id = new_mapping[gesture]
                        parts[0] = str(new_class_id)
                        break

                updated_lines.append(" ".join(parts))

        # Write the updated labels back to the file
        with open(filepath, 'w') as file:
            file.write("\n".join(updated_lines))

print("Class labels have been updated successfully!")
print(f"{index} files updated successfully!")