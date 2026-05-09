from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Real-Time IoT Anomaly Detection System"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    

settings = Settings()