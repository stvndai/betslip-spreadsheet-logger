from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model("betslip.png", conf=0.4)

for r in results:
    for box in r.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        print(cls, conf, x1, y1, x2, y2)
        
        