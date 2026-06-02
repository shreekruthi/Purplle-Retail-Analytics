import cv2

from detect import PersonDetector

VIDEO = "../data/CAM 3.mp4"

print("Loading detector...")
detector = PersonDetector()

print("Opening video...")
cap = cv2.VideoCapture(VIDEO)

if not cap.isOpened():
    print("ERROR: Cannot open video")
    exit()

print("Video opened successfully")

success, frame = cap.read()

if not success:
    print("ERROR: Could not read first frame")
    exit()

print("Frame read successfully")

detections = detector.detect(frame)

print(f"Detected {len(detections)} people")

for det in detections:

    x1, y1, x2, y2 = det["bbox"]

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

cv2.imwrite(
    "output.jpg",
    frame
)

print("Saved output.jpg")

cap.release()