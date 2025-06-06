from typing import Any
import redis.asyncio as redis
from contextlib import asynccontextmanager

from src.config import REDIS_HOST, REDIS_PORT


@asynccontextmanager
async def get_redis_client():
    """Функция для получения клиента Redis."""
    async with redis.Redis(host=REDIS_HOST, port=REDIS_PORT) as client:
        yield client


class RedisClient:
    """Класс для работы с Redis."""

    async def set(self, key: str, value: str) -> None:
        """Сохраняет объект в Redis."""
        async with get_redis_client() as client:
            await client.set(key, value)

    async def get(self, key: str) -> Any:
        """Получает сохраненный объект из Redis."""
        async with get_redis_client() as client:
            return await client.get(key)

    async def delete(self, key: str) -> bool:
        """Удаляет ключ из Redis."""
        async with get_redis_client() as client:
            return await client.delete(key)

    async def expire(self, key: str, expiration_time: int) -> None:
        """Устанавливает время жизни для ключа в Redis."""
        async with get_redis_client() as client:
            await client.expire(key, expiration_time)
