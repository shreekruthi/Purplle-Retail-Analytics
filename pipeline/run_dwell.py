import cv2

from config import (
    STORE_ID,
    VIDEOS,
    EVENT_FILE
)

from detect import (
    PersonDetector
)

from tracker import (
    VisitorTracker
)

from emit import (
    EventEmitter
)

from dwell_tracker import (
    DwellTracker
)

from zone_utils import (
    get_zone
)


CAMERA = "CAM1"

VIDEO = VIDEOS[CAMERA]


def main():

    detector = PersonDetector()

    tracker = VisitorTracker()

    emitter = EventEmitter(
        EVENT_FILE
    )

    dwell_tracker = (
        DwellTracker()
    )

    cap = cv2.VideoCapture(
        VIDEO
    )

    while True:

        success, frame = cap.read()

        if not success:
            break

        detections = (
            detector.detect(
                frame
            )
        )

        tracked = (
            tracker.update(
                detections
            )
        )

        if tracked is None:
            continue

        for box, track_id in zip(
                tracked.xyxy,
                tracked.tracker_id
        ):

            x1, y1, x2, y2 = (
                box.astype(int)
            )

            center_x = (
                x1 + x2
            ) // 2

            center_y = (
                y1 + y2
            ) // 2

            zone = get_zone(
                CAMERA,
                center_x,
                center_y
            )

            if zone:

                visitor_id = (
                    f"VIS_{track_id}"
                )

                result = (
                    dwell_tracker
                    .update(
                        visitor_id,
                        zone
                    )
                )

                if result:

                    emitter.emit(
                        store_id=
                        STORE_ID,

                        camera_id=
                        CAMERA,

                        visitor_id=
                        visitor_id,

                        event_type=
                        result[
                            "event_type"
                        ],

                        zone_id=
                        result[
                            "zone_id"
                        ],

                        dwell_ms=
                        result[
                            "dwell_ms"
                        ]
                    )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

        cv2.imshow(
            "Dwell Tracking",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()