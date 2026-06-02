from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.funnel import (
    FunnelResponse
)

from app.services.funnel_service import (
    build_funnel
)

router = APIRouter(
    prefix="/stores",
    tags=["funnel"]
)


@router.get(
    "/{store_id}/funnel",
    response_model=FunnelResponse
)
def funnel(
        store_id: str,
        db: Session = Depends(get_db)
):

    return build_funnel(
        db,
        store_id
    )