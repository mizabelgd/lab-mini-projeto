import os

SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme-use-a-strong-key-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
