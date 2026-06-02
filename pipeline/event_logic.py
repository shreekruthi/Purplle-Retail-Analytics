from collections import defaultdict
import time


class EventLogic:

    def __init__(self):

        self.first_seen = {}

        self.last_seen = {}

        self.entry_sent = set()

        self.exit_sent = set()

        self.zone_start = defaultdict(dict)

    def process_track(
            self,
            visitor_id
    ):

        now = time.time()

        if visitor_id not in self.first_seen:

            self.first_seen[
                visitor_id
            ] = now

            return "ENTRY"

        self.last_seen[
            visitor_id
        ] = now

        return None

    def process_zone(
            self,
            visitor_id,
            zone_name
    ):

        now = time.time()

        if (
                zone_name
                not in
                self.zone_start[
                    visitor_id
                ]
        ):

            self.zone_start[
                visitor_id
            ][zone_name] = now

            return None

        dwell = (
            now
            -
            self.zone_start[
                visitor_id
            ][zone_name]
        )

        if dwell >= 10:

            return {
                "event":
                "ZONE_DWELL",

                "zone":
                zone_name,

                "dwell_ms":
                int(
                    dwell * 1000
                )
            }

        return None