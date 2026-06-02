import cv2

from detect import PersonDetector
from tracker import VisitorTracker

VIDEO = "../data/CAM 3.mp4"


def main():

    print("Loading detector...")
    detector = PersonDetector()

    print("Loading tracker...")
    tracker = VisitorTracker()

    print("Opening video...")
    cap = cv2.VideoCapture(VIDEO)

    if not cap.isOpened():
        print("ERROR: Cannot open video")
        return

    while True:

        success, frame = cap.read()

        if not success:
            print("End of video")
            break

        detections = detector.detect(frame)

        tracked = tracker.update(detections)

        print("\n--------------------")
        print("TRACKED TYPE:", type(tracked))

        if tracked is None:
            print("No tracked objects")
            continue

        try:
            print("Number of tracks:", len(tracked))
        except Exception as e:
            print("Length error:", e)

        try:

            if hasattr(tracked, "xyxy"):

                for box, track_id in zip(
                        tracked.xyxy,
                        tracked.tracker_id
                ):

                    x1, y1, x2, y2 = (
                        box.astype(int)
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"VIS_{track_id}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

            else:

                print(
                    "tracked object has no xyxy attribute"
                )

                print(tracked)

        except Exception as e:

            print(
                "Tracking visualization error:"
            )

            print(e)

        cv2.imshow(
            "Tracking",
            frame
        )

        key = cv2.waitKey(1)

        if key == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()