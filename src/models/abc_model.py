"""
Модуль BaseModel определяет абстрактный базовый класс для моделей базы данных.
Предоставляет шаблон для реализации CRUD-операций.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    """Абстрактный класс для моделей базы данных с CRUD-операциями."""

    @abstractmethod
    async def create_object(self, data: dict) -> Any:
        """Создаёт новую запись в базе данных."""
        pass

    @abstractmethod
    async def read_object(self, id: int) -> Any:
        """Получает запись по ID."""
        pass

    @abstractmethod
    async def read_objects(self, page: int, limit: int) -> list[Any]:
        """Получает список записей с пагинацией."""
        pass

    @abstractmethod
    async def update_object(self, id: int, data: dict) -> Any:
        """Обновляет запись по ID."""
        pass

    @abstractmethod
    async def delete_object(self, id: int) -> Any:
        """Удаляет запись по ID."""
        pass
