import time


class QueueTracker:

    def __init__(self):

        self.entry_times = {}

        self.join_sent = set()

    def update(
            self,
            visitor_id
    ):

        now = time.time()

        if visitor_id not in self.entry_times:

            self.entry_times[
                visitor_id
            ] = now

            return None

        wait_time = (
            now
            -
            self.entry_times[
                visitor_id
            ]
        )

        if (
            wait_time >= 5
            and
            visitor_id
            not in self.join_sent
        ):

            self.join_sent.add(
                visitor_id
            )

            return {
                "event_type":
                "BILLING_QUEUE_JOIN"
            }

        return None