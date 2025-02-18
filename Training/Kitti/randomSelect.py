import os
import random
import shutil

def reduce_images_to_percentage(directory, percentage):
    # Ensure the percentage is between 0 and 100
    if percentage <= 0 or percentage > 100:
        raise ValueError("Percentage should be between 0 and 100.")

    # Get a list of all files in the directory
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Calculate the number of files to keep (2.4% of total)
    num_files_to_keep = max(1, int(len(all_files) * (percentage / 100)))

    # Randomly select files to keep
    files_to_keep = random.sample(all_files, num_files_to_keep)
    
    parent_directory = os.path.dirname(directory)
    # Create a subdirectory to move the selected files into
    selected_dir = os.path.join(parent_directory, "train_60")
    os.makedirs(selected_dir, exist_ok=True)

    # Move the selected files to the new subdirectory
    i=0
    for file in files_to_keep:
        shutil.copy2(os.path.join(directory, file), os.path.join(selected_dir, file))
        i+=1
        print(i)
        # print(directory, file, selected_dir)

    print(f"Moved {len(files_to_keep)} files to {selected_dir}.")

# Set the directory and percentage
image_directory = "/media/william/mist2/william/Github/ultralytics/dataset/KITTI/yolo/images/train"  # Replace with the actual path to your image directory
percentage_to_keep = 60

# Run the script
reduce_images_to_percentage(image_directory, percentage_to_keep)
