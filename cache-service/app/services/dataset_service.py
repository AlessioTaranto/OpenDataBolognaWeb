import aiohttp
from ..utils.redis_client import redis_client
import json
from ..models.dataset_models import DatasetResponse 

API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna?timezone=UTC&include_links=false&include_app_metas=false"

async def fetch_dataset_from_api() -> DatasetResponse:
    """
    Fetch dataset from the Opendata API and validate using Pydantic model.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return DatasetResponse(**data)
            else:
                raise Exception("Failed to fetch dataset")

async def get_dataset() -> DatasetResponse:
    """
    Get dataset from cache or fetch from API and cache the result.
    """
    cache_key = "opendata_bologna_dataset"
    
    # Try to get the data from Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return DatasetResponse(**json.loads(cached_data))
    
    # If not cached, fetch from API
    dataset = await fetch_dataset_from_api()

    # Cache the data for 1 hour (3600 seconds)
    redis_client.setex(cache_key, 3600, json.dumps(dataset.dict()))
    
    return dataset