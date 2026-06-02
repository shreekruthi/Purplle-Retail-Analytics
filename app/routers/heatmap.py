from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.heatmap import (
    HeatmapResponse
)

from app.services.heatmap_service import (
    build_heatmap
)

router = APIRouter(
    prefix="/stores",
    tags=["heatmap"]
)


@router.get(
    "/{store_id}/heatmap",
    response_model=HeatmapResponse
)
def heatmap(
        store_id: str,
        db: Session = Depends(get_db)
):

    return build_heatmap(
        db,
        store_id
    )