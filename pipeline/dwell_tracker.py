import time


class DwellTracker:

    def __init__(self):

        self.zone_entry_time = {}

        self.dwell_sent = set()

    def update(
            self,
            visitor_id,
            zone_name
    ):

        now = time.time()

        key = (
            visitor_id,
            zone_name
        )

        if key not in self.zone_entry_time:

            self.zone_entry_time[
                key
            ] = now

            return None

        dwell = (
            now
            -
            self.zone_entry_time[key]
        )

        if dwell >= 10:

            if key not in self.dwell_sent:

                self.dwell_sent.add(
                    key
                )

                return {
                    "event_type":
                    "ZONE_DWELL",

                    "zone_id":
                    zone_name,

                    "dwell_ms":
                    int(
                        dwell * 1000
                    )
                }

        return None