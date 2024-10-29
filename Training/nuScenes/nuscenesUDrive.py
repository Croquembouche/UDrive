from ultralytics import YOLO
import json
from tqdm import tqdm
from ultralytics.utils.downloads import download
from pathlib import Path
import torch

def train():
    model = YOLO("yolo11n.pt")
    results = model.train(data="/media/william/mist2/william/Github/UDrive/Training/nuScenes/nuscenesUDrive80.yaml", epochs=100, imgsz=640)

train()

