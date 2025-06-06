"""
Модуль BookController реализует контроллер для управления книгами.
Наследуется от BaseController и обеспечивает CRUD-операции для модели Book.
"""

from src.database import Book
from src.exceptions import handle_no_result_found, handle_integrity_error
from src.controllers.abc_controller import BaseController
from src.models.book import BookModel
from src.schemas.book import (
    BookCreate,
    BookUpdate,
    PaginatedBooksResponse,
    BookResponse,
)


class BookController(BaseController):
    """Контроллер для работы с книгами через CRUD-операции."""

    def __init__(self):
        """Инициализирует контроллер с моделью BookModel."""
        self.model = BookModel()

    @handle_integrity_error
    async def create_object(self, schema: BookCreate) -> Book:
        """Создаёт новую книгу в базе данных."""
        values = schema.model_dump()
        return await self.model.create_object(values)

    @handle_integrity_error
    @handle_no_result_found
    async def read_object(self, book_id: int) -> BookResponse:
        """Получает книгу по ID."""
        return BookResponse.model_validate(await self.model.read_object(book_id))

    async def read_objects(self, page: int, limit: int) -> PaginatedBooksResponse:
        """Получает список книг с пагинацией."""
        return await self.model.read_objects(page, limit)

    @handle_integrity_error
    @handle_no_result_found
    async def update_object(self, book_id: int, schema: BookUpdate) -> Book:
        """Обновляет данные книги по ID."""
        values = schema.model_dump(exclude_none=True)
        return await self.model.update_object(book_id, values)

    @handle_no_result_found
    async def delete_object(self, book_id: int) -> Book:
        """Удаляет книгу по ID."""
        return await self.model.delete_object(book_id)
