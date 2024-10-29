from ultralytics import YOLO
import json
from tqdm import tqdm
from ultralytics.utils.downloads import download
from pathlib import Path

model = YOLO("yolo11n.pt")
results = model.train(data="nuscenes.yaml", epochs=100, imgsz=640)

