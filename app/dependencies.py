from app.database import RedisDatabase
from app.queue import RedisQueue

# Create an instance of the RedisDatabase
redis_db = RedisDatabase()

# Dependency function to provide the database implementation
def get_db():
    return redis_db

def get_redis_queue():
    db = get_db()
    redis_queue = RedisQueue(redis_connection=db.client)
    return redis_queue
