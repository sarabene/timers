from rq import Queue
from app.database import RedisDatabase

# Create an instance of the RedisDatabase
redis_db = RedisDatabase()

# Dependency function to provide the database implementation
def get_db():
    return redis_db

def get_redis_queue():
    db = get_db()
    redis_queue = Queue(connection=db.client)
    return redis_queue
