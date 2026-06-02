from pydantic import BaseModel


class FunnelResponse(BaseModel):

    visitors: int

    zone_visitors: int

    queue_visitors: int

    converted_visitors: int

    visitor_to_zone: float

    zone_to_queue: float

    queue_to_purchase: float