from pydantic import BaseModel


class StoreMetricsResponse(BaseModel):

    unique_visitors: int

    total_sessions: int

    conversion_rate: float

    avg_session_minutes: float

    avg_dwell_per_zone: dict

    queue_depth: int

    abandonment_rate: float