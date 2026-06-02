from sqlalchemy import func

from app.database.tables import (
    EventRow,
    SessionRow
)
def build_funnel(
        db,
        store_id
):

    visitors = (
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
        .scalar()
        or 0
    )

    zone_visitors = (
        db.query(
            func.count(
                func.distinct(
                    EventRow.visitor_id
                )
            )
        )
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type == "ZONE_DWELL"
        )
        .scalar()
        or 0
    )

    queue_visitors = (
        db.query(
            func.count(
                func.distinct(
                    EventRow.visitor_id
                )
            )
        )
        .filter(
            EventRow.store_id == store_id
        )
        .filter(
            EventRow.event_type ==
            "BILLING_QUEUE_JOIN"
        )
        .scalar()
        or 0
    )

    converted_visitors = (
        db.query(SessionRow)
        .filter(
            SessionRow.store_id == store_id
        )
        .filter(
            SessionRow.converted == True
        )
        .count()
    )

    visitor_to_zone = (
        zone_visitors * 100 / visitors
        if visitors
        else 0
    )

    zone_to_queue = (
        queue_visitors * 100 / zone_visitors
        if zone_visitors
        else 0
    )

    queue_to_purchase = (
        converted_visitors * 100 /
        queue_visitors
        if queue_visitors
        else 0
    )

    return {
        "visitors": visitors,
        "zone_visitors": zone_visitors,
        "queue_visitors": queue_visitors,
        "converted_visitors": converted_visitors,

        "visitor_to_zone":
            round(visitor_to_zone, 2),

        "zone_to_queue":
            round(zone_to_queue, 2),

        "queue_to_purchase":
            round(queue_to_purchase, 2)
    }
