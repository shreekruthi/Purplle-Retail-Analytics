import supervision as sv
import numpy as np


class VisitorTracker:

    def __init__(self):
        self.tracker = sv.ByteTrack()

    def update(self, detections):

        if len(detections) == 0:
            return None

        xyxy = []
        confidence = []

        for det in detections:
            xyxy.append(det["bbox"])
            confidence.append(det["confidence"])

        detections_sv = sv.Detections(
            xyxy=np.array(xyxy),
            confidence=np.array(confidence),
            class_id=np.zeros(len(xyxy), dtype=int)
        )

        tracked = self.tracker.update_with_detections(
            detections_sv
        )

        return tracked