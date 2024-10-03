import os
import shutil

# Define the directory containing the subfolders
source_directory = '/media/william/blueicedrive/Github/UDrive/Analysis/ArgoVerse1/images'  # Replace this with the path to your main folder
destination_directory = '/media/william/blueicedrive/Github/UDrive/Analysis/ArgoVerse1/combined'  # Replace this with the path where you want to move all images

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Traverse the directory
for subdir, dirs, files in os.walk(source_directory):
    for file in files:
        # Check if the file is an image (e.g., jpg or png)
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            file_path = os.path.join(subdir, file)
            destination_path = os.path.join(destination_directory, file)
            
            # Move the file to the destination folder
            shutil.move(file_path, destination_path)

print(f"All images have been moved to {destination_directory}")
