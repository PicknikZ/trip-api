from .base import Settings

class TestSettings(Settings):
    DATABASE_URL: str = "mysql+asyncmy://root:root@localhost:3306/trip"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week
    ACCESS_TOKEN_TTL: int = 60
    DEBUG: bool = True
    ALLOWED_HOSTS: list = [
      "http://localhost",
      "http://localhost:3000",
      "http://localhost:8000",
    ]