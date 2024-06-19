from functools import partial

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_model_config = partial(SettingsConfigDict, env_file=".env", extra="ignore")


class LoggingSettings(BaseSettings):
    model_config = _model_config(env_prefix="LOGGING_")

    level: str = Field(default="INFO", init=False)
    json_format: bool = Field(default=False, init=False)


class C3Settings(BaseSettings):
    model_config = _model_config(env_prefix="C3_")

    access_key: str = Field(init=False)
    secret_key: str = Field(init=False)
    encode_secret_key: bytes = Field(init=False)
    bucket_name: str = Field(init=False)
    url: str = Field(init=False)


class AppSettings(BaseSettings):
    model_config = _model_config(env_prefix="APP_")

    name: str = Field(init=False)
    version: str = Field(init=False)
    debug: bool = Field(default=False, init=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    log: LoggingSettings = LoggingSettings()
    c3: C3Settings = C3Settings()


settings = Settings()
