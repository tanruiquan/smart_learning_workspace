from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JUDGE0_HOST: str
    JUDGE0_KEY: str
    MONGODB_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
