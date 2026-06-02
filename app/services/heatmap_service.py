from sqlalchemy import func

from app.database.tables import EventRow


def build_heatmap(
        db,
        store_id
):

    rows = (
        db.query(
            EventRow.zone_id,
            func.sum(
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

    if not rows:

        return {
            "zones": {}
        }

    zone_totals = {}

    max_dwell = max(
        dwell
        for _, dwell in rows
    )

    for zone, dwell in rows:

        score = (
            dwell * 100 / max_dwell
        )

        zone_totals[zone] = round(
            score,
            2
        )

    return {
        "zones": zone_totals
    }