import os
import shutil

def keep_and_move_specific_images(source_folder, target_folder):
    # List all image files, assuming they're JPEGs. Adjust the extension if needed.
    image_files = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]
    image_files.sort()  # Ensure the files are sorted
    
    total_images = len(image_files)
    
    # Initialize the list with the first image's index
    indices_to_keep = [0]
    
    # Add every 30th image to the list
    for i in range(1, total_images, 30):
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

def process_and_move_scenarios(folder, target):
    count = 0
    os.makedirs(folder, exist_ok=True)
    for image_name in os.listdir(folder):
        # Ensure the target directory exists
        if image_name.startswith("n008"):
            # if count % 30 == 0:
            image_path = os.path.join(folder, image_name)
            target_path = os.path.join(target, image_name)
            shutil.copy2(image_path, target_path)
            print(image_path)
            # count += 1
    print("Done")





# Specify the path to the 'train_1' folder and the target base folder
folder = '/media/william/blueicedrive/datasets/NuScenes/v1.0-trainval09_blobs_camera/samples/CAM_FRONT'
target = '/media/william/blueicedrive/datasets/NuScenes/annotated_images'
process_and_move_scenarios(folder, target)
