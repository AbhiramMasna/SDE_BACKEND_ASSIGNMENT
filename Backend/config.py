import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/image_db")
REDIS_BROKER = os.getenv("REDIS_BROKER", "redis://localhost:6379/0")
