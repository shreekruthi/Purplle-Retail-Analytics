from app.database.tables import (
    EventRow,
    SessionRow
)
def detect_anomalies(
        db,
        store_id
):

    anomalies = []

    joins = (
        db.query(EventRow)
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type ==
            "BILLING_QUEUE_JOIN"
        )
        .count()
    )

    abandons = (
        db.query(EventRow)
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type ==
            "BILLING_QUEUE_ABANDON"
        )
        .count()
    )

    queue_depth = joins - abandons

    if queue_depth >= 5:

        anomalies.append({
            "type": "QUEUE_SPIKE",
            "severity": "HIGH",
            "message":
            f"Queue depth is {queue_depth}"
        })

    sessions = (
        db.query(SessionRow)
        .filter(
            SessionRow.store_id == store_id
        )
        .count()
    )

    converted = (
        db.query(SessionRow)
        .filter(
            SessionRow.store_id == store_id
        )
        .filter(
            SessionRow.converted == True
        )
        .count()
    )

    if sessions:

        conversion = (
            converted * 100 / sessions
        )

        if conversion < 10:

            anomalies.append({
                "type":
                "CONVERSION_DROP",

                "severity":
                "MEDIUM",

                "message":
                f"Conversion only {conversion:.2f}%"
            })

    zone_events = (
        db.query(EventRow)
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type ==
            "ZONE_DWELL"
        )
        .count()
    )

    if zone_events == 0:

        anomalies.append({
            "type":
            "DEAD_ZONE",

            "severity":
            "LOW",

            "message":
            "No customer activity detected"
        })

    return {
        "anomalies":
        anomalies
    }