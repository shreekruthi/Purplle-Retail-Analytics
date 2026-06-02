from sqlalchemy import func

from app.database.tables import (
    EventRow,
    SessionRow
)
def unique_visitors(
        db,
        store_id
):

    return (
        db.query(
            func.count(
                func.distinct(
                    SessionRow.visitor_id
                )
            )
        )
        .filter(
            SessionRow.store_id == store_id
        )
        .filter(
            SessionRow.is_staff == False
        )
        .scalar()
        or 0
    )
def total_sessions(
        db,
        store_id
):

    return (
        db.query(SessionRow)
        .filter(
            SessionRow.store_id == store_id
        )
        .count()
    )
def conversion_rate(
        db,
        store_id
):

    total = (
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

    if total == 0:
        return 0

    return round(
        converted * 100 / total,
        2
    )
def avg_session_minutes(
        db,
        store_id
):

    sessions = (
        db.query(SessionRow)
        .filter(
            SessionRow.store_id == store_id
        )
        .all()
    )

    if not sessions:
        return 0

    total_minutes = 0

    count = 0

    for session in sessions:

        if (
            session.entry_time
            and
            session.exit_time
        ):

            diff = (
                session.exit_time
                -
                session.entry_time
            )

            total_minutes += (
                diff.total_seconds()
                / 60
            )

            count += 1

    if count == 0:
        return 0

    return round(
        total_minutes / count,
        2
    )
def avg_dwell_per_zone(
        db,
        store_id
):

    rows = (
        db.query(
            EventRow.zone_id,
            func.avg(
                EventRow.dwell_ms
            )
        )
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type ==
            "ZONE_DWELL"
        )
        .group_by(
            EventRow.zone_id
        )
        .all()
    )

    return {
        zone: round(
            avg / 1000,
            2
        )
        for zone, avg in rows
        if zone
    }
def queue_depth(
        db,
        store_id
):

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

    return max(
        joins - abandons,
        0
    )
def abandonment_rate(
        db,
        store_id
):

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

    if joins == 0:
        return 0

    return round(
        abandons * 100 / joins,
        2
    )
