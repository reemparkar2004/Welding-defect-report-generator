from ultralytics import YOLO

model = YOLO("best.pt")

print(model.names)

def detect_defect(image_path):
    results = model(image_path, conf=0.25)
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls)
            detections.append({
                "defect": model.names[cls_id],
                "confidence": float(box.conf)
            })

    return detections
