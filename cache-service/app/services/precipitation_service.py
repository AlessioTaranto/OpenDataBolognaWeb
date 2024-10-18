import aiohttp
import json
from datetime import datetime, timedelta
from utils.redis_client import redis_client
from ..models.precipitaion_model import PrecipitationResponse, WeeklyPrecipitationResponse
from utils.date_utils import get_week_range

PRECIPITATION_API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna/records"

async def fetch_precipitation_data(start_date: datetime, end_date: datetime) -> PrecipitationResponse:
    params = {
        'where': f"date >= '{start_date.date().isoformat()}' AND date <= '{end_date.date().isoformat()}'",
        'limit': 100,
        'timezone': 'UTC',
        'include_links': 'false',
        'include_app_metas': 'false'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(PRECIPITATION_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return PrecipitationResponse(**data)
            else:
                raise Exception("Failed to fetch precipitation data")

async def get_weekly_precipitation(date: datetime) -> WeeklyPrecipitationResponse:
    week_start, week_end = get_week_range(date)
    cache_key = f"precipitation_data_{week_start.isoformat()}_{week_end.isoformat()}"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return WeeklyPrecipitationResponse(**json.loads(cached_data))
    
    precipitation_data = await fetch_precipitation_data(week_start, week_end)
    
    weekly_response = WeeklyPrecipitationResponse(
        week_start=week_start,
        week_end=week_end,
        records=precipitation_data.results
    )
    
    redis_client.setex(cache_key, 86400, json.dumps(weekly_response.dict()))
    
    return weekly_response