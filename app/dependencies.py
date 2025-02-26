from app.database import RedisDatabase
from app.job_queue import RedisQueue

# Create an instance of the RedisDatabase
redis_db = RedisDatabase()


def get_db():
    """Dependency function to return a RedisDatabase instance"""
    return redis_db


def get_redis_queue():
    """Dependency function to return a RedisQueue instance"""
    db = get_db()
    redis_queue = RedisQueue(redis_connection=db.client)
    return redis_queue
