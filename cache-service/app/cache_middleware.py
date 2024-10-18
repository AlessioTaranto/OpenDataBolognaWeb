from .utils.redis_client import redis_client

async def cache_middleware(cache_key: str, fetch_function):
    """
    General caching middleware that checks if data is cached in Redis and serves it if available.
    Otherwise, it calls the fetch_function to get fresh data.

    :param cache_key: The key to store the data in Redis
    :param fetch_function: The function to call to fetch the data if it's not cached
    :return: The cached or fresh data
    """
    # Check if cache exists
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # If it does, return the cached data
        return cached_data
    
    # If not cached, call the fetch function
    fresh_data = await fetch_function()

    # Cache the fresh data for 1 hour
    redis_client.setex(cache_key, 3600, str(fresh_data))

    # Return the fresh data
    return fresh_data

