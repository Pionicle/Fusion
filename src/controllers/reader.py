"""
Модуль ReaderController реализует контроллер для управления читателями.
Наследуется от BaseController и обеспечивает CRUD-операции для модели Reader.
"""

from src.database import Reader
from src.exceptions import (
    handle_no_result_found,
    handle_integrity_error,
)
from src.controllers.abc_controller import BaseController
from src.models.reader import ReaderModel
from src.schemas.reader import (
    ReaderCreate,
    ReaderUpdate,
    PaginatedReadersResponse,
    ReaderResponse,
)


class ReaderController(BaseController):
    """Контроллер для работы с читателями через CRUD-операции."""

    def __init__(self):
        """Инициализирует контроллер с моделью ReaderModel."""
        self.model = ReaderModel()

    @handle_integrity_error
    async def create_object(self, schema: ReaderCreate) -> Reader:
        """Создаёт нового читателя в базе данных."""
        values = schema.model_dump()
        return await self.model.create_object(values)

    @handle_integrity_error
    @handle_no_result_found
    async def read_object(self, reader_id: int) -> ReaderResponse:
        """Получает читателя по ID."""
        return ReaderResponse.model_validate(await self.model.read_object(reader_id))

    async def read_objects(self, page: int, limit: int) -> PaginatedReadersResponse:
        """Получает список читателей с пагинацией."""
        return await self.model.read_objects(page, limit)

    @handle_integrity_error
    @handle_no_result_found
    async def update_object(self, reader_id: int, schema: ReaderUpdate) -> Reader:
        """Обновляет данные читателя по ID."""
        values = schema.model_dump(exclude_none=True)
        return await self.model.update_object(reader_id, values)

    @handle_no_result_found
    async def delete_object(self, reader_id: int) -> Reader:
        """Удаляет читателя по ID."""
        return await self.model.delete_object(reader_id)

    @handle_integrity_error
    @handle_no_result_found
    async def add_book_to_reader(self, reader_id: int, book_id: int) -> Reader:
        """Добавляет книгу к читателю."""
        return await self.model.add_book_to_reader(reader_id, book_id)

    @handle_integrity_error
    @handle_no_result_found
    async def remove_book_from_reader(self, reader_id: int, book_id: int) -> Reader:
        """Удаляет книгу у читателя."""
        return await self.model.remove_book_from_reader(reader_id, book_id)
