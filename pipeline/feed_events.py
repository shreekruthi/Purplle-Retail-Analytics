import json
import requests


def feed_events(
        file_path,
        api_url
):

    events = []

    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if line:

                events.append(
                    json.loads(line)
                )

    if not events:

        print(
            "No events found"
        )

        return

    response = requests.post(
        f"{api_url}/events/ingest",
        json=events,
        timeout=60
    )

    print(
        response.status_code
    )

    print(
        response.text
    )