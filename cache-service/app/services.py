import aiohttp
from redis_client import redis_client  # Import the redis_client from your module

API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets"

async def fetch_datasets_from_api():
    """
    Fetch datasets from the Opendata API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']  # Assuming datasets are in the 'results' field
            else:
                raise Exception("Failed to fetch datasets")

async def get_datasets():
    """
    Get datasets from cache or fetch from API and cache the result.
    """
    cache_key = "opendata_bologna_datasets"
    
    # Try to get the data from Redis cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Serving from cache")
        return cached_data
    
    # If not cached, fetch from API
    datasets = await fetch_datasets_from_api()

    # Cache the data for 1 hour (3600 seconds)
    redis_client.setex(cache_key, 3600, str(datasets))
    
    return datasets
