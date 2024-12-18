from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_KEY: str = "your-api-key"
    DATABASE_URL: str = "postgresql://user:password@db:5432/transactions_db"
    REDIS_URL: str = "redis://localhost:6379/0"
def get_settings():
    return Settings()

