import os
import shutil

def keep_and_move_specific_images(source_folder, target_folder):
    # List all image files, assuming they're JPEGs. Adjust the extension if needed.
    image_files = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]
    image_files.sort()  # Ensure the files are sorted
    
    total_images = len(image_files)
    
    # Initialize the list with the first image's index
    indices_to_keep = [0]
    
    # Add every 100th image to the list
    for i in range(1, total_images, 50):
        indices_to_keep.append(i)
    
    # Ensure the last image is included, if it's not already
    if total_images - 1 not in indices_to_keep:
        indices_to_keep.append(total_images - 1)

    # Ensure the target directory exists
    os.makedirs(target_folder, exist_ok=True)

    # Copy selected files to the target directory
    for index in indices_to_keep:
        source_path = os.path.join(source_folder, image_files[index])
        target_path = os.path.join(target_folder, image_files[index])
        shutil.copy2(source_path, target_path)

def process_and_move_scenarios(base_folder, target_base):
    for scenario_id in os.listdir(base_folder):
        scenario_path = os.path.join(base_folder, scenario_id)
        if os.path.isdir(scenario_path):
            # Construct the path to the images' directory. Adjust this path as needed for your structure.
            image_data_path = os.path.join(scenario_path, 'ring_front_center')  # Updated for the new structure
            if os.path.exists(image_data_path):
                # Prepare the target folder path using the scenario ID
                target_folder = os.path.join(target_base, scenario_id)
                keep_and_move_specific_images(image_data_path, target_folder)


# Specify the path to the 'train_1' folder and the target base folder
base_folder = '/media/carla/blueicedrive/ArgoVerse/1/tracking_train4_v1.1/argoverse-tracking/train4'
target_base = '/home/carla/Github/UDrive/Analysis/ArgoVerse1/images'
process_and_move_scenarios(base_folder, target_base)

print("Processed all scenarios. Moved first, median, and last images to the target location.")
