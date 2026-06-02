from pydantic import BaseModel


class Anomaly(BaseModel):

    type: str

    severity: str

    message: str


class AnomalyResponse(BaseModel):

    anomalies: list[Anomaly]