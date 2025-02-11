from ultralytics import YOLO

model = YOLO("yolo11n.pt")
results = model.train(data="Cityscapes20.yaml", epochs=200, imgsz=640, device=[3])