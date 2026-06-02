from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.metrics import (
    StoreMetricsResponse
)

from app.services.metrics_service import *

router = APIRouter(
    prefix="/stores",
    tags=["metrics"]
)


@router.get(
    "/{store_id}/metrics",
    response_model=StoreMetricsResponse
)
def metrics(
        store_id: str,
        db: Session = Depends(get_db)
):

    return StoreMetricsResponse(

        unique_visitors=
        unique_visitors(
            db,
            store_id
        ),

        total_sessions=
        total_sessions(
            db,
            store_id
        ),

        conversion_rate=
        conversion_rate(
            db,
            store_id
        ),

        avg_session_minutes=
        avg_session_minutes(
            db,
            store_id
        ),

        avg_dwell_per_zone=
        avg_dwell_per_zone(
            db,
            store_id
        ),

        queue_depth=
        queue_depth(
            db,
            store_id
        ),

        abandonment_rate=
        abandonment_rate(
            db,
            store_id
        )
    )