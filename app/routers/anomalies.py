from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.anomaly import (
    AnomalyResponse
)

from app.services.anomaly_service import (
    detect_anomalies
)

router = APIRouter(
    prefix="/stores",
    tags=["anomalies"]
)


@router.get(
    "/{store_id}/anomalies",
    response_model=AnomalyResponse
)
def anomalies(
        store_id: str,
        db: Session = Depends(get_db)
):

    return detect_anomalies(
        db,
        store_id
    )