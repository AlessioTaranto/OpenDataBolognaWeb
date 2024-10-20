# Bologna Dataset Cache API

This project implements a FastAPI-based web service to fetch and cache datasets from the **Opendata API** for Bologna using **Redis**. It caches the dataset results for improved performance, and it allows selecting specific datasets by ID.

## Features

- Fetches datasets from the **Opendata API** for Bologna.
- Caches dataset responses in **Redis** for 1 hour.
- Provides an endpoint to select and retrieve a specific dataset by its ID.
- Implements an efficient caching mechanism using Redis to reduce load on the external API.

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
4. [API Endpoints](#api-endpoints)
5. [Project Structure](#project-structure)
6. [Technologies Used](#technologies-used)

## Installation

To get started with this project, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/bologna-dataset-cache-api.git
   cd bologna-dataset-cache-api
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have **Redis** installed and running. You can install Redis using the following command (for Linux):

   ```bash
   sudo apt-get install redis
   ```

   Alternatively, use Docker:

   ```bash
   docker run -d -p 6379:6379 redis
   ```

## Environment Setup

1. Create a `.env` file in the project root directory and add your Redis configuration:

   ```env
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

2. (Optional) Add any API keys or environment variables you may need.

## Running the Application

1. Start the **FastAPI** application using **Uvicorn**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## API Endpoints

### 1. Fetch all datasets

**GET** `/datasets`

Fetches all available datasets from the **Opendata API** and caches the response in **Redis** for 1 hour.

**Example request:**

```bash
GET http://localhost:8000/datasets
```

**Example response:**

```json
{
  "datasets": [
    {
      "dataset_id": "temperature_bologna",
      "dataset_name": "Bologna Weather Data",
      "description": "Temperature data for Bologna",
      ...
    },
    ...
  ]
}
```

### 2. Fetch a specific dataset by ID

**GET** `/datasets/{dataset_id}`

Fetches a specific dataset from the cached datasets using the `dataset_id`.

**Example request:**

```bash
GET http://localhost:8000/datasets/temperature_bologna
```

**Example response:**

```json
{
  "dataset": {
    "dataset_id": "temperature_bologna",
    "dataset_name": "Bologna Weather Data",
    "description": "Temperature data for Bologna",
    ...
  }
}
```

### Error Response

If a dataset is not found:

```json
{
  "detail": "Dataset not found"
}
```

## Project Structure

```bash
/your_project
│
├── /app
│   ├── main.py            # Main FastAPI app
│   ├── redis_client.py     # Redis configuration
│   ├── services.py         # Service to fetch datasets from Opendata API
│   ├── cache_middleware.py # Cache middleware for Redis
│   └── models.py           # Optional: Pydantic models for data validation
├── .env                    # Environment variables (Redis connection details)
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Technologies Used

- **FastAPI**: High-performance framework for building APIs.
- **Redis**: In-memory data structure store used for caching.
- **aiohttp**: Async HTTP client for fetching data from external APIs.
- **uvicorn**: ASGI server for serving FastAPI applications.
- **Pydantic**: Data validation and settings management using Python type hints.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.
