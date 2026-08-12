from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[1]


class AppConfig(BaseSettings):
    app_name: str = Field(default="FastShop")
    app_env: str = Field(default="local")
    app_debug: bool = Field(default=True)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_timezone: str = Field(default="Asia/Tehran")
    app_url: str = Field(default="http://127.0.0.1:8000")

    model_config = SettingsConfigDict(
        env_file=_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
