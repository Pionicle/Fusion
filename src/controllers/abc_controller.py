"""
Модуль BaseController определяет абстрактный класс для контроллеров,
обеспечивающих взаимодействие между маршрутами API и моделями базы данных.
Реализует шаблон для CRUD-операций.
"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel as BaseSchema


class BaseController(ABC):
    """Абстрактный класс для контроллеров с CRUD-операциями."""

    @abstractmethod
    async def create_object(self, schema: BaseSchema) -> Any:
        """Создаёт запись в базе данных по схеме."""
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
    async def update_object(self, id: int, model: BaseSchema) -> Any:
        """Обновляет запись по ID."""
        pass

    @abstractmethod
    async def delete_object(self, id: int) -> bool:
        """Удаляет запись по ID."""
        pass
