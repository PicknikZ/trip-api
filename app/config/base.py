import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    API_V1_STR: str = "/v1"
