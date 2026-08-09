from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    jwt_secret: str = Field(default="secret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=60)