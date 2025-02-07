import os
from os import walk, getcwd
import json
from typing import List, Any
from PIL import Image
from tqdm import tqdm
import argparse
import cv2
import numpy as np


label_path = "/media/william/blueicedrive/Github/2D_label_parser/labels/"
image_path = "/media/william/blueicedrive/datasets/NuScenes/annotated_images/n008-2018-05-21-11-06-59-0400__CAM_FRONT__1526915293412465.jpg"

import cv2

# Function to display image with bounding box
def displayImage(image_path, bbox_corners):
    # Load the image
    image = cv2.imread(image_path)

    # Ensure the image is loaded
    if image is None:
        print(f"Error: Could not load image {image_path}")
        return

    # # Unpack bbox_corners (x_min, x_max, y_min, y_max)
    # x_min, y_min, x_max, y_max = bbox_corners

    # # Convert floating point to integers (pixel values)
    # x_min = int(x_min*1800)
    # x_max = int(x_max*1800)
    # y_min = int(y_min*900)
    # y_max = int(y_max*900)

    # Unpack bbox_corners (x, y, w, h)
    x, y, w, h = bbox_corners

    # Convert floating point to integers (pixel values)
    x_min = int((x-w/2)*1800)
    x_max = int((x+w/2)*1800)
    y_min = int((y-h/2)*900)
    y_max = int((y+h/2)*900)

    # Draw the bounding box on the image using the coordinates
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color=(0, 255, 0), thickness=2)

    # Show the image with the bounding box
    cv2.imshow("Bounding Box", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Test data: bbox_corners and image path
bbox_corners = [0.10070463668337663, 0.5143771867324058, 0.20140927336675327, 0.13549643982435575]

# Call the function to display the image with the bbox
displayImage(image_path, bbox_corners)

