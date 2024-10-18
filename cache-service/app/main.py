from fastapi import FastAPI, HTTPException
from .models.dataset_models import DatasetResponse
from .models.precipitation_model import PrecipitationResponse
from .services.dataset_service import get_dataset
from .services.precipitation_service import get_weekly_precipitation
from datetime import datetime

app = FastAPI()

@app.get("/dataset", response_model=DatasetResponse)
async def get_bologna_dataset() -> DatasetResponse:
    """
    Endpoint to fetch and return the Bologna precipitation dataset.

    :return: The Bologna precipitation dataset.
    :rtype: DatasetResponse
    """
    try:
        # Call the get_dataset service to fetch the dataset
        dataset = await get_dataset()

        # Return the dataset
        return dataset

    except Exception as e:
        # If an exception occurs, raise an HTTPException
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/precipitation", response_model=PrecipitationResponse)
async def get_weekly_precipitation_data(date: str):
    """
    Endpoint to fetch weekly precipitation data.

    :param date: The date for which to fetch the weekly precipitation data.
    :type date: str
    :return: The weekly precipitation data.
    :rtype: WeeklyPrecipitationResponse
    """
    try:
        print("Fetching weekly precipitation data for " + date)
        # Convert the date from a string to a datetime object
        start_date = datetime.strptime(date, "%Y-%m-%d")

        # Fetch the weekly precipitation data
        precipitation_data = await get_weekly_precipitation(start_date)

        # Return the fetched data
        print("Fetched data: " + str(precipitation_data))
        return precipitation_data.model_dump()
    except ValueError as e:
        print("Error: " + str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print("Error: " + str(e))
        # Raise an error if any other exception occurs
        raise HTTPException(status_code=500, detail=str(e))
    