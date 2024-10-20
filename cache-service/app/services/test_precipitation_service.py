import pytest
import aiohttp
from unittest.mock import patch, AsyncMock
from datetime import datetime
from ..utils.redis_client import redis_client
from ..models.precipitation_model import PrecipitationResponse
from .precipitation_service import fetch_precipitation_data, get_weekly_precipitation  # Adjust the import as needed
from ..utils.date_utils import get_week_range

PRECIPITATION_API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna/records"

@pytest.mark.asyncio
async def test_fetch_precipitation_data():
    """
    Test the fetch_precipitation_data function.

    This test uses a mocked API response to ensure that the fetch_precipitation_data
    function correctly fetches and validates the precipitation data from the Opendata API.
    It checks if the returned data is an instance of PrecipitationResponse and matches
    the expected mock response data.
    """
    mock_response_data = {
        # Add mock data that matches the structure expected by PrecipitationResponse
    }
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 7)
    
    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response_data)
        
        precipitation_data = await fetch_precipitation_data(start_date, end_date)
        
        assert isinstance(precipitation_data, PrecipitationResponse)
        assert precipitation_data == PrecipitationResponse(**mock_response_data)

@pytest.mark.asyncio
async def test_get_weekly_precipitation():
    """
    Test the get_weekly_precipitation function.

    This test uses a mocked API response to ensure that the get_weekly_precipitation
    function correctly fetches and caches the weekly precipitation data from the
    Opendata API. It checks if the returned data is an instance of PrecipitationResponse
    and matches the expected mock response data, and also verifies that the data was
    cached in Redis with the correct key and expiration time.
    """
    mock_response_data = {
        # Add mock data that matches the structure expected by PrecipitationResponse
    }
    
    date = datetime(2023, 1, 1)
    week_start, week_end = get_week_range(date)
    
    with patch('redis_client.get', return_value=None):
        with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 200
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response_data)
            
            precipitation_data = await get_weekly_precipitation(date)
            
            assert isinstance(precipitation_data, PrecipitationResponse)
            assert precipitation_data == PrecipitationResponse(**mock_response_data)
            
            # Check if the data was cached
            redis_client.setex.assert_called_once_with(f"precipitation_data_{week_start}_{week_end}", 86400, json.dumps(precipitation_data.model_dump()))

@pytest.mark.asyncio
async def test_get_weekly_precipitation_from_cache():
    """
    Test the get_weekly_precipitation function when data is retrieved from cache.

    This test verifies that the get_weekly_precipitation function correctly fetches
    the weekly precipitation data from the Redis cache when available, without
    making an API call. It checks if the returned data is an instance of
    PrecipitationResponse and matches the expected mock cached data from Redis.
    """
    mock_cached_data = {
        # Add mock data that matches the structure expected by PrecipitationResponse
    }
    
    date = datetime(2023, 1, 1)
    week_start, week_end = get_week_range(date)
    
    with patch('redis_client.get', return_value=json.dumps(mock_cached_data)):
        precipitation_data = await get_weekly_precipitation(date)
        
        assert isinstance(precipitation_data, PrecipitationResponse)
        assert precipitation_data == PrecipitationResponse(**mock_cached_data)
