import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")  # 'n' stands for nano version, you can use 's', 'm', 'l', 'x' for different sizes

# Initialize video capture
cap = cv2.VideoCapture(0)  # 0 for webcam, or provide the path to a video file

# Tracking with Centroid
def centroid_tracking(objects, boxes):
    new_objects = {}
    object_id = 0
    
    for box in boxes:
        x, y, w, h = box
        cx = x + w // 2
        cy = y + h // 2
        same_object = False

        for id, pt in objects.items():
            dx, dy = abs(cx - pt[0]), abs(cy - pt[1])
            if dx < 50 and dy < 50:  # Threshold for object association
                new_objects[id] = (cx, cy)
                same_object = True
                break

        if not same_object:
            new_objects[object_id] = (cx, cy)
            object_id += 1

    return new_objects

# Tracking ID for objects
objects = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Perform detection using YOLOv8
    results = model(frame)  # Perform inference on the current frame
    detections = results[0]  # The first result contains the detections

    boxes = []
    for detection in detections.boxes:
        x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Get bounding box coordinates
        w, h = x2 - x1, y2 - y1
        boxes.append([x1, y1, w, h])
        
        # Convert the tensor to a Python data type
        cls = int(detection.cls)
        conf = float(detection.conf)

        label = f"{cls}, {conf:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Object tracking
    objects = centroid_tracking(objects, boxes)
    
    for id, pt in objects.items():
        cx, cy = pt
        cv2.putText(frame, f"ID {id}", (cx - 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

    # Display frame
    cv2.imshow("Object Detection and Tracking", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
