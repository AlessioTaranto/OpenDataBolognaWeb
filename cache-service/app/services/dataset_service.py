import aiohttp
from ..utils.redis_client import redis_client
import json
from ..models.dataset_models import DatasetResponse 

API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna?timezone=UTC&include_links=false&include_app_metas=false"

async def fetch_dataset_from_api() -> DatasetResponse:
    """
    Fetch dataset from the Opendata API and validate using Pydantic model.

    :return DatasetResponse: A Pydantic model representing the dataset.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                data = await response.json()
                # Validate the response using the Pydantic model
                return DatasetResponse(**data)
            else:
                # Raise an exception if the request fails
                raise Exception("Failed to fetch dataset")

async def get_dataset() -> DatasetResponse:
    """
    Get the dataset from cache or fetch it from the API and cache the result.

    The dataset is cached for 1 hour (3600 seconds) in Redis to avoid
    re-fetching the data on every request.

    :return DatasetResponse: A Pydantic model representing the dataset.
    """
    cache_key = "opendata_bologna_dataset"
    
    # Try to get the data from Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # If the data is cached, return it as a Pydantic model
        return DatasetResponse(**json.loads(cached_data))
    
    # If not cached, fetch the dataset from the API
    dataset = await fetch_dataset_from_api()

    # Cache the data for 1 hour (3600 seconds)
    redis_client.setex(cache_key, 3600, json.dumps(dataset.model_dump()))
    
    # Return the dataset
    return dataset
