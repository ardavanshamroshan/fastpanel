from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[1]


class LoggingConfig(BaseSettings):
    log_channel: str = Field(default="single")
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_path: str = Field(default=f"{_ROOT}/storage/app/logs/app.log")

    model_config = SettingsConfigDict(
        env_file=_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def channels(self) -> dict:
        """
        Return the channels configuration.
        """
        return {
            "single": {
                "driver": "single",
                "path": self.log_path,
                "level": self.log_level,
                "format": self.log_format,
            },
        }
