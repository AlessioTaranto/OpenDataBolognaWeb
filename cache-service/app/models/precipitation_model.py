from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PrecipitationRecord(BaseModel):
    date: str
    avg_184_d: float
    stagione: str

class PrecipitationResponse(BaseModel):
    total_count: int
    results: List[PrecipitationRecord]
