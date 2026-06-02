import cv2

from config import (
    STORE_ID,
    VIDEOS,
    EVENT_FILE
)

from detect import PersonDetector
from tracker import VisitorTracker
from emit import EventEmitter
from queue_tracker import QueueTracker


CAMERA = "CAM5"
VIDEO = VIDEOS[CAMERA]


def main():

    print(f"Starting Queue Analytics for {CAMERA}")

    detector = PersonDetector()

    tracker = VisitorTracker()

    emitter = EventEmitter(
        EVENT_FILE
    )

    queue_tracker = QueueTracker()

    cap = cv2.VideoCapture(
        VIDEO
    )

    if not cap.isOpened():

        print(
            f"Cannot open {VIDEO}"
        )

        return

    while True:

        success, frame = cap.read()

        if not success:

            print(
                "End of video"
            )

            break

        detections = detector.detect(
            frame
        )

        tracked = tracker.update(
            detections
        )

        if tracked is None:
            continue

        if len(tracked) == 0:
            continue

        for box, track_id in zip(
                tracked.xyxy,
                tracked.tracker_id
        ):

            visitor_id = (
                f"VIS_{track_id}"
            )

            result = (
                queue_tracker.update(
                    visitor_id
                )
            )

            if result:

                emitter.emit(
                    store_id=STORE_ID,

                    camera_id=CAMERA,

                    visitor_id=visitor_id,

                    event_type=result[
                        "event_type"
                    ]
                )

            x1, y1, x2, y2 = (
                box.astype(int)
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                visitor_id,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.imshow(
            "Billing Queue Analytics",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()