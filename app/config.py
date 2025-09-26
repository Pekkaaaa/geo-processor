from pydantic_settings import BaseSettings
from decouple import Csv, config


class Settings(BaseSettings):
    app_name: str = config("APP_NAME", default="Geo Processor")
    debug: bool = config("DEBUG", default=False)
    api_key: str = config("API_KEY", default="")
    public_paths: str = config("PUBLIC_PATHS", default="/health,/openapi.json,/docs,/redoc", cast=Csv())

    class Config:
        env_file = ".env"

settings = Settings()
