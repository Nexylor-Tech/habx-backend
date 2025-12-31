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

    @field_validator("ALLOW_ORIGINS", mode="before")
    def parse_allow_origins(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return v


settings = Settings()
