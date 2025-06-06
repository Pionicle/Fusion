"""
Модуль для хранения настроек.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Хранит переменные конфига из файала .env.
    """

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def database_url(self):
        """
        Строка подключения к базе данных.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

DATABASE_URL = settings.database_url

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
