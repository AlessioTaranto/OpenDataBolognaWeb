from fastapi import FastAPI, HTTPException
from models import Dataset
from services import get_dataset

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