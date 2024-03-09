import os
import shutil

def keep_and_copy_images(source_folder, target_folder, interval=50):
    # Ensure the target directory exists
    os.makedirs(target_folder, exist_ok=True)
    
    # List and sort image files
    image_files = sorted([f for f in os.listdir(source_folder) if f.endswith('.png')])

    # Determine which images to keep: start with the first, every 100th, and include the last
    indices_to_keep = [0] + list(range(interval-1, len(image_files), interval))
    # Ensure the last image is included, avoiding duplication if it's already in the list
    if len(image_files) - 1 not in indices_to_keep:
        indices_to_keep.append(len(image_files) - 1)

    # Copy selected images to the target folder
    for index in indices_to_keep:
        src_path = os.path.join(source_folder, image_files[index])
        dst_path = os.path.join(target_folder, image_files[index])
        shutil.copy2(src_path, dst_path)

def process_drive_folders(base_folder, output_base):
    for drive_id in os.listdir(base_folder):
        drive_path = os.path.join(base_folder, drive_id)
        if os.path.isdir(drive_path):
            image_data_path = os.path.join(drive_path, 'image_02', 'data')
            if os.path.exists(image_data_path):
                # Prepare the target folder path, maintaining the drive folder structure
                target_folder = os.path.join(output_base, drive_id)
                keep_and_copy_images(image_data_path, target_folder)

# Paths to the source '2011_09_26' folder and the target location where folders should be created
base_folder = '/media/carla/blueicedrive/kitti/2011_09_30'
new_location = '/home/carla/Github/UDrive/Analysis/Kitti/images'

process_drive_folders(base_folder, new_location)

print("Done processing all drive folders. First, median, and last images have been copied.")
