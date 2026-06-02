from sqlalchemy.orm import Session

from app.database.tables import EventRow
from app.services.session_service import (
        create_session,
        close_session,
        update_session_dwell
)

def save_event(
        db: Session,
        payload: dict
):

    existing = db.get(
        EventRow,
        payload["event_id"]
    )

    if existing:
        return "duplicate"

    row = EventRow(
        event_id=payload["event_id"],
        store_id=payload["store_id"],
        camera_id=payload["camera_id"],
        visitor_id=payload["visitor_id"],
        event_type=payload["event_type"],
        zone_id=payload.get("zone_id"),
        dwell_ms=payload.get("dwell_ms", 0),
        is_staff=payload.get("is_staff", False),
        confidence=payload["confidence"],
        timestamp=payload["timestamp"],
        metadata_json=payload.get("metadata", {})
    )

    db.add(row)
    if payload["event_type"] == "ENTRY":
    
        create_session(
            db,
            row
        )

    elif payload["event_type"] == "EXIT":

        close_session(
            db,
            row
        )

    elif payload["event_type"] == "ZONE_DWELL":

        update_session_dwell(
            db,
            row
        )
    

    return "inserted"

