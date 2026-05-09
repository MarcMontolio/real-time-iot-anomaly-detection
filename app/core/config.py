from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    app_name: str
    app_env: str 
    debug: bool 
    api_v1_prefix: str
    database_url: str
    database_sync_url: str
    redis_url: str
    mqtt_host: str
    mqtt_port: int
    log_level: str

settings = Settings()