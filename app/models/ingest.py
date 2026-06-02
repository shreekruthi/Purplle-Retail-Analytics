from pydantic import BaseModel


class IngestResponse(BaseModel):

    received: int

    inserted: int

    duplicates: int

    failed: int

    errors: list = []