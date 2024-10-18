import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=0,
    decode_responses=True
)
