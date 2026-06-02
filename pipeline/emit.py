import json
import uuid
from datetime import datetime


class EventEmitter:

    def __init__(self, output_file):

        self.output_file = output_file

    def emit(
            self,
            store_id,
            camera_id,
            visitor_id,
            event_type,
            zone_id=None,
            dwell_ms=0
    ):

        event = {
            "event_id": str(uuid.uuid4()),
            "store_id": store_id,
            "camera_id": camera_id,
            "visitor_id": visitor_id,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "zone_id": zone_id,
            "dwell_ms": dwell_ms,
            "is_staff": False,
            "confidence": 1.0,
            "metadata": {}
        }

        with open(
                self.output_file,
                "a",
                encoding="utf-8"
        ) as f:

            f.write(
                json.dumps(event)
            )

            f.write("\n")

        print(
            f"[EVENT] {event_type} -> {visitor_id}"
        )