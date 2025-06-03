"""
Модуль AuthorController реализует контроллер для управления авторами.
Наследуется от BaseController и обеспечивает CRUD-операции для модели Author.
"""

from src.database import Author
from src.exceptions import handle_no_result_found
from src.controllers.abc_controller import BaseController
from src.models.author import AuthorModel
from src.schemas.author import (
    AuthorCreate,
    AuthorUpdate,
    PaginatedAuthorsResponse,
)


class AuthorController(BaseController):
    """Контроллер для работы с авторами через CRUD-операции."""

    def __init__(self):
        """Инициализирует контроллер с моделью AuthorModel."""
        self.model = AuthorModel()

    async def create_object(self, schema: AuthorCreate) -> Author:
        """Создаёт нового автора в базе данных."""
        values = schema.model_dump()
        return await self.model.create_object(values)

    @handle_no_result_found
    async def read_object(self, author_id: int) -> Author:
        """Получает автора по ID."""
        return await self.model.read_object(author_id)

    async def read_objects(self, page: int, limit: int) -> PaginatedAuthorsResponse:
        """Получает список авторов с пагинацией."""
        return await self.model.read_objects(page, limit)

    @handle_no_result_found
    async def update_object(self, author_id: int, schema: AuthorUpdate) -> Author:
        """Обновляет данные автора по ID."""
        values = schema.model_dump(exclude_none=True)
        return await self.model.update_object(author_id, values)

    @handle_no_result_found
    async def delete_object(self, author_id: int) -> Author:
        """Удаляет автора по ID."""
        return await self.model.delete_object(author_id)
