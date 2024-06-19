from functools import partial

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_model_config = partial(SettingsConfigDict, env_file=".env", extra="ignore")


class DBSettings(BaseSettings):
    model_config = _model_config(env_prefix="DB_")

    password: SecretStr = Field(init=False)
    user: SecretStr = Field(init=False)
    host: str = Field(init=False)
    port: int = Field(default=5432, init=False)
    db_name: str = Field(default="video", init=False)

    def get_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user.get_secret_value()}:"
            f"{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"
        )


class LoggingSettings(BaseSettings):
    model_config = _model_config(env_prefix="LOGGING_")

    level: str = Field(default="INFO", init=False)
    json_format: bool = Field(default=False, init=False)


class C3Settings(BaseSettings):
    model_config = _model_config(env_prefix="FARPOST_")

    upload_url: str = Field(init=False)


class AppSettings(BaseSettings):
    model_config = _model_config(env_prefix="APP_")

    name: str = Field(init=False)
    version: str = Field(init=False)
    debug: bool = Field(default=False, init=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DBSettings = DBSettings()
    log: LoggingSettings = LoggingSettings()
    c3: C3Settings = C3Settings()


settings = Settings()
