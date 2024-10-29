import json
from tqdm import tqdm
from ultralytics.utils.downloads import download
from pathlib import Path

def argoverse2yolo(set):
    labels = {}
    a = json.load(open(set, "rb"))
    for annot in tqdm(a['annotations'], desc=f"Converting {set} to YOLOv5 format..."):
        img_id = annot['image_id']
        img_name = a['images'][img_id]['name']
        img_label_name = f'{img_name[:-3]}txt'

        cls = annot['category_id']  # instance class id
        x_center, y_center, width, height = annot['bbox']
        x_center = (x_center + width / 2) / 1920.0  # offset and scale
        y_center = (y_center + height / 2) / 1200.0  # offset and scale
        width /= 1920.0  # scale
        height /= 1200.0  # scale
        img_dir = Path("/media/william/mist2/william/Github/ultralytics/dataset/Argoverse-1.1/labels/")
        seq_dir = a['seq_dirs'][a['images'][img_id]['sid']]
        img_dir = img_dir / seq_dir
        if not img_dir.exists():
            img_dir.mkdir(parents=True, exist_ok=True)

        k = str(img_dir / img_label_name)
        if k not in labels:
            labels[k] = []
        labels[k].append( f"{cls} {x_center} {y_center} {width} {height}\n")

    for k in labels:
        with open(k, "w") as f:
            f.writelines(labels[k])


# Download 'https://argoverse-hd.s3.us-east-2.amazonaws.com/Argoverse-HD-Full.zip' (deprecated S3 link)
# dir = "/media/william/mist2/william/Github/ultralytics/dataset/" # dataset root dir
# # Convert
# annotations_dir = "/media/william/mist2/william/Github/ultralytics/dataset/Argoverse-HD/labels"
# for d in annotations_dir+"/train.json", annotations_dir+"/val.json":
#     argoverse2yolo(d)  # convert Argoverse annotations to YOLO labels

import os
import shutil
def folderRestructure():
    # Specify the target directory (default is current directory)
    target_dir = "dataset/Argoverse-UDrive/images/train/"
    # print(folder_path)

    # Check if the target directory exists
    if not os.path.exists(target_dir):
        print(f"The specified directory does not exist: {target_dir}")
        exit(1)

    # # Create the folder if it doesn't exist
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
    #     print(f"Folder '{folder_name}' created in {target_dir}.")

    # Move all files from target directory to the new folder
    for foldername in os.listdir(target_dir):

        folderpath = os.path.join(target_dir, foldername)
        # create a new folder
        ring_path = os.path.join(folderpath, "ring_front_center")
        if not os.path.exists(ring_path):
            os.makedirs(ring_path)
            print(f"Folder '{ring_path}' created in {folderpath}.")
        for file in os.listdir(folderpath):
            
            file_path = os.path.join(folderpath, file)
            if os.path.isfile(file_path):
                moved_path = os.path.join(ring_path, file)
                shutil.move(file_path, moved_path)


    # print(f"All files moved to {folder_path}.")
# folderRestructure()