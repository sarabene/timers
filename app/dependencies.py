from app.database import RedisDatabase

# Create an instance of the RedisDatabase
redis_db = RedisDatabase()

# Dependency function to provide the database implementation
def get_db():
    return redis_db