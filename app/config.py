from dotenv import load_dotenv
from pydantic import AnyUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    MONGO_URL: SecretStr
    GEMINI_API_KEY: SecretStr
    ALLOW_ORIGINS: list[str] = ["*"]
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: SecretStr
    # dodo
    DODO_API_KEY: SecretStr
    DODO_API_KEY_TEST: SecretStr
    DODO_WEBHOOK_SECRET: SecretStr
    DODO_ENVIRONMENT: str

    # Subscription
    PRODUCT_ID_PREMIUM: str
    PRODUCT_ID_ELITE: str

    AI_LIMITS: dict[str, int] = {"free": 10, "premium": 30, "elite": 100}

    @field_validator("ALLOW_ORIGINS", mode="before")
    def parse_allow_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


settings = Settings()
