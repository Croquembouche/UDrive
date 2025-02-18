from ultralytics import YOLO

model = YOLO("yolo11n.pt")
results = model.train(data="CityscapesFull.yaml", epochs=200, imgsz=640, device=[0])