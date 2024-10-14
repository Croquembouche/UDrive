from ultralytics import YOLO
import json
from tqdm import tqdm
from ultralytics.utils.downloads import download
from pathlib import Path
import torch

def train():
    model = YOLO("yolo11n.pt")
    results = model.train(data="ArgoverseUDrive.yaml", epochs=100, imgsz=640)

train()

