from pathlib import Path

from pydantic import BaseModel, Field

_ROOT = Path(__file__).resolve().parents[1]


class LoggingConfig(BaseModel):
    log_channel: str = Field(default="single")
    log_level: str = Field(default="INFO")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_path: str = Field(default=f"{_ROOT}/storage/app/logs/app.log")

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
