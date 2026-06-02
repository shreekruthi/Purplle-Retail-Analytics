from pydantic import BaseModel


class HeatmapResponse(BaseModel):

    zones: dict