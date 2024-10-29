import os
import shutil
import random

# Paths
source_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/images/annotated_images'       # Directory with images
labels_train_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels/train'  # Directory with training labels
labels_test_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels/test'    # Directory with test labels
labels_val_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels/val'      # Directory with validation labels
train_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/images/train'          # Target train directory
test_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/images/test'            # Target test directory
val_dir = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/images/val'              # Target validation directory
source_label_dir = "/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels/CAM_FRONT"
# Create target directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Get all image files
label_files = [f for f in os.listdir(source_label_dir) if f.endswith(('.txt'))]

# Shuffle the image files
random.shuffle(label_files)

# Calculate split sizes
total_images = len(label_files)
train_size = int(total_images * 0.024)
# test_size = int(total_images * 0.2)
# val_size = total_images - train_size - test_size

# Split the images
train_labels = label_files[:train_size]
# test_labels = label_files[train_size:train_size + test_size]
# val_labels = label_files[train_size + test_size:]

# Function to move files to the target directory
def move_files(file_list, target_image_dir, target_label_dir, source_label_dir):
    for label_file in file_list:      
        # Move corresponding label
        if label_file.startswith("n008"):
            image_file = os.path.splitext(label_file)[0] + '.jpg'  # Assuming label files are .txt
            current_image_path = os.path.join(source_dir, image_file)
            target_image_path = os.path.join(target_image_dir, image_file)
            current_label_path = os.path.join(source_label_dir, label_file)
            target_label_path = os.path.join(target_label_dir, label_file)
            # print(current_image_path, target_image_path, current_label_path, target_label_path)
            if os.path.exists(current_image_path):
                # print("image exist ready to move")      
                shutil.move(current_image_path, target_image_path)
                shutil.move(current_label_path, target_label_path)

# Move files to respective directories
move_files(train_labels, train_dir, labels_train_dir, source_label_dir)
# move_files(test_labels, test_dir, labels_test_dir, source_label_dir)
# move_files(val_labels, val_dir, labels_val_dir, source_label_dir)

# print("Files have been distributed successfully.")
# Define paths to the folders
folders = ['train', 'test', 'val']  # Folders to be processed
cam_front_folder = '/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels/CAM_FRONT'      # Folder containing the new labels

# Define the function to replace label files
def replace_labels(folders, cam_front_folder):
    # Loop over each folder (train, test, val)
    for folder in folders:
        folder_path = os.path.join("/media/william/mist2/william/Github/ultralytics/dataset/nuScenesFullNA/labels", folder)
        
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder '{folder}' does not exist.")
            continue

        # Loop through the files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Make sure it's a file (not a directory)
            if os.path.isfile(file_path):
                # Define the path to the new label file in CAM_FRONT
                new_label_path = os.path.join(cam_front_folder, file_name)

                # Check if the corresponding label exists in CAM_FRONT
                if os.path.exists(new_label_path):
                    # Replace the old label with the new one
                    shutil.copy(new_label_path, file_path)
                    print(f"Replaced {file_path} with {new_label_path}")
                else:
                    print(f"No matching label found for {file_name} in CAM_FRONT.")
            else:
                print(f"{file_name} is not a valid file.")

# Call the function to replace labels
# replace_labels(folders, cam_front_folder)
