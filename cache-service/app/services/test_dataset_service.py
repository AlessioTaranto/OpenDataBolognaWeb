import pytest
import aiohttp
from unittest.mock import patch, AsyncMock
from ..utils.redis_client import redis_client
from ..models.dataset_models import DatasetResponse
from .dataset_service import fetch_dataset_from_api, get_dataset  # Adjust the import as needed

API_URL = "https://opendata.comune.bologna.it/api/explore/v2.1/catalog/datasets/precipitazioni_bologna?timezone=UTC&include_links=false&include_app_metas=false"

@pytest.mark.asyncio
async def test_fetch_dataset_from_api():
    """
    Test the fetch_dataset_from_api function.

    This test uses a mocked API response to ensure that the fetch_dataset_from_api
    function correctly fetches and validates the dataset from the Opendata API.
    It checks if the returned dataset is an instance of DatasetResponse and matches
    the expected mock response data.
    """
    mock_response_data = {
        # Add mock data that matches the structure expected by DatasetResponse
    }
    
    with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response_data)
        
        dataset = await fetch_dataset_from_api()
        
        assert isinstance(dataset, DatasetResponse)
        assert dataset == DatasetResponse(**mock_response_data)

@pytest.mark.asyncio
async def test_get_dataset():
    """
    Test the get_dataset function.

    This test uses a mocked API response to ensure that the get_dataset
    function correctly fetches and caches the dataset from the Opendata API.
    It checks if the returned dataset is an instance of DatasetResponse and matches
    the expected mock response data, and also verifies that the data was cached
    in Redis with the correct key and expiration time.
    """
    mock_response_data = {
        # Add mock data that matches the structure expected by DatasetResponse
    }
    
    with patch('redis_client.get', return_value=None):
        with patch('aiohttp.ClientSession.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 200
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response_data)
            
            dataset = await get_dataset()
            
            assert isinstance(dataset, DatasetResponse)
            assert dataset == DatasetResponse(**mock_response_data)
            
            # Check if the data was cached
            redis_client.setex.assert_called_once_with("opendata_bologna_dataset", 3600, json.dumps(dataset.model_dump()))

@pytest.mark.asyncio
async def test_get_dataset_from_cache():
    """
    Test the get_dataset function when data is retrieved from cache.

    This test verifies that the get_dataset function correctly fetches
    the dataset from the Redis cache when available, without making an
    API call. It checks if the returned dataset is an instance of
    DatasetResponse and matches the expected mock cached data from Redis.
    """
    mock_cached_data = {
        # Add mock data that matches the structure expected by DatasetResponse
    }
    
    with patch('redis_client.get', return_value=json.dumps(mock_cached_data)):
        dataset = await get_dataset()
        
        assert isinstance(dataset, DatasetResponse)
        assert dataset == DatasetResponse(**mock_cached_data)
