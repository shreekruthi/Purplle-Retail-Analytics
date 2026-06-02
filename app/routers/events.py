from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.event import StoreEvent
from app.models.ingest import IngestResponse

from app.services.ingestion_service import save_event
from enum import Enum

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post(
    "/ingest",
    response_model=IngestResponse
)
def ingest_events(
        events: list[StoreEvent],
        db: Session = Depends(get_db)
):

    inserted = 0
    duplicates = 0
    failed = 0

    errors = []

    for idx, event in enumerate(events):

        try:

            result = save_event(
                db,
                event.model_dump()
            )

            if result == "duplicate":
                duplicates += 1
            else:
                inserted += 1

        except Exception as ex:

            failed += 1

            errors.append({
                "index": idx,
                "error": str(ex)
            })

    db.commit()

    return IngestResponse(
        received=len(events),
        inserted=inserted,
        duplicates=duplicates,
        failed=failed,
        errors=errors
    )
class EventType(str, Enum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ZONE_ENTER = "ZONE_ENTER"
    ZONE_EXIT = "ZONE_EXIT"
    ZONE_DWELL = "ZONE_DWELL"
    BILLING_QUEUE_JOIN = "BILLING_QUEUE_JOIN"
    BILLING_QUEUE_ABANDON = "BILLING_QUEUE_ABANDON"
    REENTRY = "REENTRY"