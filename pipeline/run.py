import cv2
import os

from config import (
    STORE_ID,
    VIDEOS,
    EVENT_FILE
)

from detect import PersonDetector
from tracker import VisitorTracker
from emit import EventEmitter
from event_logic import EventLogic


CAMERA = "CAM3"
VIDEO = VIDEOS[CAMERA]


def main():

    print("\n========== DEBUG ==========")
    print("Current Working Directory:")
    print(os.getcwd())

    print("\nSelected Camera:")
    print(CAMERA)

    print("\nVideo Path:")
    print(VIDEO)

    print("\nAbsolute Path:")
    print(os.path.abspath(VIDEO))

    print("\nFile Exists:")
    print(os.path.exists(VIDEO))
    print("===========================\n")

    detector = PersonDetector()
    tracker = VisitorTracker()
    emitter = EventEmitter(EVENT_FILE)
    logic = EventLogic()

    cap = cv2.VideoCapture(VIDEO)

    print("cap.isOpened() =", cap.isOpened())

    if not cap.isOpened():

        print("\nERROR: Cannot open video")
        print("Check the path above.")

        return

    print("Video opened successfully")

    while True:

        success, frame = cap.read()

        if not success:
            print("End of video reached")
            break

        detections = detector.detect(frame)

        tracked = tracker.update(detections)

        if tracked is None:
            continue

        if len(tracked) == 0:
            continue

        for box, track_id in zip(
                tracked.xyxy,
                tracked.tracker_id
        ):

            visitor_id = f"VIS_{track_id}"

            event = logic.process_track(
                visitor_id
            )

            if event:

                emitter.emit(
                    store_id=STORE_ID,
                    camera_id=CAMERA,
                    visitor_id=visitor_id,
                    event_type=event
                )

            x1, y1, x2, y2 = box.astype(int)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                visitor_id,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Retail Analytics",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:
            print("ESC pressed")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()