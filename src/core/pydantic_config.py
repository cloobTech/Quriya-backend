from pydantic_settings import BaseSettings, SettingsConfigDict


class PydanticConfig(BaseSettings):
    """Base configuration for Pydantic models."""

    DEV_ENV: str = "development"  # dev, uat, production
    REDIS_URL: str = "redis://localhost:6379"
    RESEND_API_KEY: str = ""
    MAIL_FROM: str = ""
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "SECRET_KEY"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


config = PydanticConfig()
