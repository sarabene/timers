import os

class Config:
    
    ENV = os.getenv('ENV', 'development')

    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
