import redis_client

async def cache_middleware(cache_key: str, fetch_function):
    """
    General caching middleware that checks if data is cached in Redis and serves it if available.
    Otherwise, it calls the fetch_function to get fresh data.
    """
    # Check if cache exists
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return cached_data
    
    # If not cached, call the fetch function
    fresh_data = await fetch_function()

    # Cache the fresh data for 1 hour
    redis_client.setex(cache_key, 3600, str(fresh_data))

    return fresh_data
