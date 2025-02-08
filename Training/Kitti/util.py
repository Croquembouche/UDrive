# import os
# import shutil
# import random

# # Define paths
# base_image_dir = "/mnt/nas/Kitti/data_object_image_2/training/image_2"  # Original folder containing images
# base_label_dir = "/media/william/mist2/william/Github/yolov7-on-cityscapes-with-bbox-cropping/scripts/labels_with_dont_care"  # Original folder containing labels

# # Define output directories for images
# train_image_dir = "/mnt/nas/Kitti/yolo/images/train"
# val_image_dir = "/mnt/nas/Kitti/yolo/images/val"
# test_image_dir = "/mnt/nas/Kitti/yolo/images/test"

# # Define output directories for labels
# train_label_dir = os.path.join("labels", "train")
# val_label_dir = os.path.join("labels", "val")
# test_label_dir = os.path.join("labels", "test")

# # Define output directories for labels (separate folder)
# labels_base_output_dir = "/mnt/nas/Kitti/yolo/labels"
# train_label_dir = os.path.join(labels_base_output_dir, "train")
# val_label_dir = os.path.join(labels_base_output_dir, "val")
# test_label_dir = os.path.join(labels_base_output_dir, "test")

# # Create necessary directories
# for folder in [train_image_dir, val_image_dir, test_image_dir, train_label_dir, val_label_dir, test_label_dir]:
#     os.makedirs(folder, exist_ok=True)

# # Get list of all images
# all_images = [f for f in os.listdir(base_image_dir) if os.path.isfile(os.path.join(base_image_dir, f))]

# # Shuffle images randomly
# random.shuffle(all_images)

# # Split indices
# total_images = len(all_images)
# train_count = int(0.6 * total_images)
# val_count = int(0.2 * total_images)

# train_images = all_images[:train_count]
# val_images = all_images[train_count:train_count + val_count]
# test_images = all_images[train_count + val_count:]

# # Function to move files safely
# def move_file(src_dir, dst_dir, filename):
#     src_path = os.path.join(src_dir, filename)
#     dst_path = os.path.join(dst_dir, filename)
#     if os.path.exists(src_path):
#         shutil.move(src_path, dst_path)

# # Move images and corresponding labels
# for img in train_images:
#     move_file(base_image_dir, train_image_dir, img)
#     label_file = os.path.splitext(img)[0] + ".txt"
#     move_file(base_label_dir, train_label_dir, label_file)

# for img in val_images:
#     move_file(base_image_dir, val_image_dir, img)
#     label_file = os.path.splitext(img)[0] + ".txt"
#     move_file(base_label_dir, val_label_dir, label_file)

# for img in test_images:
#     move_file(base_image_dir, test_image_dir, img)
#     label_file = os.path.splitext(img)[0] + ".txt"
#     move_file(base_label_dir, test_label_dir, label_file)

# print(f"Total images: {total_images}")
# print(f"Train: {len(train_images)}, Validation: {len(val_images)}, Test: {len(test_images)}")
# print("Dataset split successfully!")

import os
import shutil

# Define paths for image directories
image_base_dir = "yolo/images"
train_image_dir = os.path.join(image_base_dir, "train")
val_image_dir = os.path.join(image_base_dir, "val")
test_image_dir = os.path.join(image_base_dir, "test")

# Define the source folder where labels are stored
base_label_dir = "/mnt/nas/Kitti/yolo/labels_with_dont_care"

# Define output directories for labels
labels_base_output_dir = "labels"
train_label_dir = os.path.join(labels_base_output_dir, "train")
val_label_dir = os.path.join(labels_base_output_dir, "val")
test_label_dir = os.path.join(labels_base_output_dir, "test")

# Create necessary directories for labels
for folder in [train_label_dir, val_label_dir, test_label_dir]:
    os.makedirs(folder, exist_ok=True)

# Function to move labels based on image filenames
def move_labels(image_dir, label_output_dir):
    image_filenames = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    
    for img in image_filenames:
        label_file = os.path.splitext(img)[0] + ".txt"  # Assuming label has same name as image with .txt extension
        label_path = os.path.join(base_label_dir, label_file)
        
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(label_output_dir, label_file))

# Move labels based on images present in each folder
move_labels(train_image_dir, train_label_dir)
move_labels(val_image_dir, val_label_dir)
move_labels(test_image_dir, test_label_dir)

print("Labels have been successfully organized!")
