from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    app_name: str = Field(default="FastShop")
    app_env: str = Field(default="local")
    app_debug: bool = Field(default=True)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_timezone: str = Field(default="Asia/Tehran")
    app_url: str = Field(default="http://127.0.0.1:8000")
