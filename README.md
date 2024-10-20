# Bologna Dataset Cache API

This project implements a FastAPI-based web service to fetch and cache datasets from the **Opendata API** for Bologna using **Redis**. It caches the dataset results for improved performance, and it allows selecting specific datasets by ID.

## Features

- Fetches datasets and catalogs from the **Opendata API** for Bologna.
- Implements an efficient caching mechanism using Redis to reduce load on the external API.

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
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

## Technologies Used

- **FastAPI**: High-performance framework for building APIs.
- **Redis**: In-memory data structure store used for caching.
- **aiohttp**: Async HTTP client for fetching data from external APIs.
- **uvicorn**: ASGI server for serving FastAPI applications.
- **Pydantic**: Data validation and settings management using Python type hints.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.
