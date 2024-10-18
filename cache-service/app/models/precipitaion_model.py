from pydantic import BaseModel
from typing import List
from datetime import date

class PrecipitationRecord(BaseModel):
    date: date
    avg_184_d: float
    stagione: str

class PrecipitationResponse(BaseModel):
    total_count: int
    results: List[PrecipitationRecord]

class WeeklyPrecipitationResponse(BaseModel):
    week_start: date
    week_end: date
    records: List[PrecipitationRecord]