from .utils.redis_client import redis_client

async def cache_middleware(cache_key: str, fetch_function):
    """
    General caching middleware that checks if data is cached in Redis and serves it if available.
    Otherwise, it calls the fetch_function to get fresh data.

    :param cache_key: The key to store the data in Redis
    :param fetch_function: The function to call to fetch the data if it's not cached
    :return: The cached or fresh data
    """
    print(f"Checking cache for '{cache_key}'")
    # Check if cache exists
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Found cached data")
        # If it does, return the cached data
        return cached_data
    
    print("No cached data found")
    # If not cached, call the fetch function
    fresh_data = await fetch_function()
    print(f"Received fresh data: {fresh_data}")

    # Cache the fresh data for 1 hour
    print(f"Storing in cache with key '{cache_key}' for 1 hour")
    redis_client.setex(cache_key, 3600, str(fresh_data))

    # Return the fresh data
    return fresh_data

