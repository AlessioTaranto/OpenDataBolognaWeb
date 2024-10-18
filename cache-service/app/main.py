from fastapi import FastAPI, HTTPException
from .models.dataset_models import Dataset
from .models.precipitaion_model import WeeklyPrecipitationResponse
from .services.dataset_service import get_dataset
from .services.precipitation_service import get_weekly_precipitation
from datetime import datetime

app = FastAPI()

@app.get("/dataset", response_model=Dataset)
async def get_bologna_dataset():
    """
    Endpoint to fetch and return the Bologna precipitation dataset.
    """
    try:
        dataset = await get_dataset()
        return dataset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/precipitation", response_model=WeeklyPrecipitationResponse)
async def get_weekly_precipitation_data(date: str):
    """
    Endpoint to fetch weekly precipitation data.
    """
    try:
        start_date = datetime.fromisoformat(date)
        precipitation_data = await get_weekly_precipitation(start_date)
        return precipitation_data
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))