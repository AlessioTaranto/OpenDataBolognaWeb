import aiohttp
import json
from datetime import datetime
from ..utils.redis_client import redis_client
from ..models.precipitation_model import PrecipitationResponse, WeeklyPrecipitationResponse
from ..utils.date_utils import get_week_range

PRECIPITATION_API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna/records"

async def fetch_precipitation_data(start_date: datetime, end_date: datetime) -> PrecipitationResponse:
    """
    Fetches precipitation data from the Bologna Open Data API for a given date range.

    :param start_date: The start date of the range to fetch data for.
    :param end_date: The end date of the range to fetch data for.
    :return: A PrecipitationResponse model containing the fetched data.
    :raises Exception: If the API request fails.
    """
    params = {
        'where': f"date >= '{start_date}' AND date <= '{end_date}'",  # Set the date range for the query
        'limit': 100,  # Limit the number of records fetched
        'timezone': 'UTC',  # Specify the timezone
        'include_links': 'false',  # Exclude additional links from the response
        'include_app_metas': 'false'  # Exclude application metadata from the response
    }
    
    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Make a GET request to the API with specified parameters
        async with session.get(PRECIPITATION_API_URL, params=params) as response:
            if response.status == 200:
                # Parse the JSON response and validate it with the Pydantic model
                data = await response.json()
                return PrecipitationResponse(**data)
            else:
                # Raise an exception if the request fails
                raise Exception("Failed to fetch precipitation data")

async def get_weekly_precipitation(date: datetime) -> WeeklyPrecipitationResponse:
    """
    Retrieves weekly precipitation data, either from the cache or by fetching it.
    
    If the data is not cached, it fetches it from the Bologna Open Data API using
    the fetch_precipitation_data function.
    
    Finally, it caches the result for 24 hours (86400 seconds) in Redis.
    """
    week_start, week_end = get_week_range(date)
    cache_key = f"precipitation_data_{week_start}_{week_end}"
    
    # Check if the data is cached
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # If the data is cached, return it as a Pydantic model
        return WeeklyPrecipitationResponse(**json.loads(cached_data))
    
    # Fetch data from the API if not cached
    precipitation_data = await fetch_precipitation_data(week_start, week_end)
    
    weekly_response = WeeklyPrecipitationResponse(
        week_start=week_start,
        week_end=week_end,
        records=precipitation_data.results
    )

    # Cache the result for 24 hours (86400 seconds)
    redis_client.setex(cache_key, 86400, json.dumps(weekly_response.dict()))

    return weekly_response
