import uuid

from app.database.tables import (
    SessionRow
)


def create_session(
        db,
        event
):

    session = SessionRow(
        session_id=str(
            uuid.uuid4()
        ),

        store_id=event.store_id,

        visitor_id=event.visitor_id,

        entry_time=event.timestamp,

        is_staff=event.is_staff,

        converted=False,

        zones_visited=[]
    )

    db.add(session)

    return session
def close_session(
        db,
        event
):

    session = (
        db.query(SessionRow)
        .filter(
            SessionRow.visitor_id
            == event.visitor_id
        )
        .filter(
            SessionRow.exit_time
            == None
        )
        .first()
    )

    if session:

        session.exit_time = (
            event.timestamp
        )

    return session
def update_session_dwell(
        db,
        event
):

    session = (
        db.query(SessionRow)
        .filter(
            SessionRow.visitor_id
            == event.visitor_id
        )
        .filter(
            SessionRow.exit_time
            == None
        )
        .first()
    )

    if not session:
        return

    session.total_dwell_ms += (
        event.dwell_ms
    )

    zones = (
        session.zones_visited
        or []
    )

    if (
        event.zone_id
        and event.zone_id
        not in zones
    ):
        zones.append(
            event.zone_id
        )

    session.zones_visited = zones