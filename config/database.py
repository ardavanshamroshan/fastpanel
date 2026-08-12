from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[1]


class DatabaseConfig(BaseSettings):
    db_connection: str = Field(default="postgresql")
    db_driver: str = Field(default="psycopg")
    db_host: str = Field(default="127.0.0.1")
    db_port: int = Field(default=5432)
    db_database: str = Field(default="fastshop")
    db_username: str = Field(default="root")
    db_password: str = Field(default="password")
    db_charset: str = Field(default="utf8")

    model_config = SettingsConfigDict(
        env_file=_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """
        Return the database URL based on the connection and driver.
        Example: postgresql+psycopg://root:password@127.0.0.1:5432/database
        """
        return (
            f"{self.db_connection}+{self.db_driver}://"
            f"{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_database}"
        )

    @property
    def databases(self) -> dict:
        """
        Return the databases configuration.
        Example:
        {
            "default": "postgresql+psycopg://root:password@127.0.0.1:5432/database",
            "connections": {
                "pgsql": {
                    "driver": "postgresql",
                    "url": "postgresql+psycopg://root:password@127.0.0.1:5432/database",
                },
            },
        """
        return {
            "default": self.database_url,
            "connections": {
                "pgsql": {
                    "driver": "postgresql",
                    "url": self.database_url,
                    "host": self.db_host,
                    "port": self.db_port,
                    "database": self.db_database,
                    "username": self.db_username,
                    "password": self.db_password,
                    "charset": self.db_charset,
                    "schema": "public",
                },
                "mysql": {
                    "driver": "mysql",
                    "url": self.database_url,
                    "host": self.db_host,
                    "port": self.db_port,
                    "database": self.db_database,
                    "username": self.db_username,
                    "password": self.db_password,
                    "charset": self.db_charset,
                    "schema": "public",
                },
                "sqlite": {
                    "driver": "sqlite",
                    "url": self.database_url,
                    "host": self.db_host,
                    "port": self.db_port,
                    "database": self.db_database,
                    "username": self.db_username,
                    "password": self.db_password,
                    "charset": self.db_charset,
                    "schema": "public",
                },
            },
        }
