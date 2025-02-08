from ultralytics import YOLO
import json
from tqdm import tqdm
from ultralytics.utils.downloads import download
from pathlib import Path

model = YOLO("yolo11n.pt")
results = model.val(data="/media/william/blueicedrive/Github/UDrive/Training/Argoverse1/Argoverse.yaml")
print(results)
