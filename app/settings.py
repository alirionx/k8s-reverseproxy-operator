import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_port: int | None = int( os.environ.get("APP_PORT", "5000"))
    app_mode: str | None = os.environ.get("APP_MODE", "prod")
    

settings = Settings()
