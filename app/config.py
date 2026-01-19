from pydantic import AnyUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")
    MONGO_URL: SecretStr
    GEMINI_API_KEY: SecretStr
    ALLOW_ORIGINS: list[str] = ["*"]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: SecretStr
    CLERK_PEM_PUBLIC_KEY: SecretStr
    # dodo
    DODO_API_KEY: SecretStr
    DODO_WEBHOOK_SECRET: SecretStr
    DODO_ENVIRONMENT: str
    DODO_BASE_URL: AnyUrl

    # Subscription
    PRODUCT_ID_PREMIUM: str
    PRODUCT_ID_ELITE: str
    
    AI_LIMITS: dict = {"free": 10, "premium": 30, "elite": 100}
    WORKSPACE_LIMITS: dict = {"free": 1, "premium": 20, "elite": 100}

    @field_validator("ALLOW_ORIGINS", mode="before")
    def parse_allow_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


settings = Settings()
