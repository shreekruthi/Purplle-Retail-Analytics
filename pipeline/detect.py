import cv2

from ultralytics import YOLO

from config import (
    YOLO_MODEL,
    CONFIDENCE_THRESHOLD
)


class PersonDetector:

    def __init__(self):

        self.model = YOLO(
            YOLO_MODEL
        )

    def detect(
            self,
            frame
    ):

        results = self.model(
            frame,
            classes=[0],
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                )

                confidence = float(
                    box.conf[0]
                )

                detections.append(
                    {
                        "bbox": [
                            int(x1),
                            int(y1),
                            int(x2),
                            int(y2)
                        ],

                        "confidence":
                        confidence
                    }
                )

        return detections