from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    RMQ_URL: str
    REDIS_URL: str
    DB_URL: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str


settings = Settings()
