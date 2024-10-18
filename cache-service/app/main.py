from fastapi import FastAPI, HTTPException
from services import get_datasets

app = FastAPI()

@app.get("/datasets")
async def get_bologna_datasets():
    """
    Endpoint to fetch and return datasets, with Redis caching.
    """
    try:
        datasets = await get_datasets()
        return {"datasets": datasets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For selecting a specific dataset
@app.get("/datasets/{dataset_id}")
async def get_dataset_by_id(dataset_id: str):
    """
    Endpoint to fetch a specific dataset by its ID.
    """
    datasets = await get_datasets()  # Reuse the cached datasets
    selected_dataset = next((dataset for dataset in datasets if dataset["dataset_id"] == dataset_id), None)
    
    if selected_dataset:
        return {"dataset": selected_dataset}
    else:
        raise HTTPException(status_code=404, detail="Dataset not found")
