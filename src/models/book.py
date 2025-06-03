"""
Модуль BookModel реализует модель для работы с книгами в базе данных.
Наследуется от BaseModel и обеспечивает CRUD-операции с использованием SQLAlchemy.
"""

from sqlalchemy import insert, select, update, delete, func
from math import ceil

from src.models.abc_model import BaseModel
from src.database import get_async_session, Book
from src.schemas.book import PaginatedBooksResponse


class BookModel(BaseModel):
    """Модель для работы с книгами в базе данных через CRUD-операции."""

    async def create_object(self, data: dict) -> Book:
        """Создаёт новую книгу в базе данных."""
        async with get_async_session() as session:
            stmt = insert(Book).values(data).returning(Book)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def read_object(self, id: int) -> Book:
        """Получает книгу по ID."""
        async with get_async_session() as session:
            stmt = select(Book).where(Book.book_id == id)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def read_objects(self, page: int, limit: int) -> PaginatedBooksResponse:
        """Получает список книг с пагинацией."""
        async with get_async_session() as session:
            stmt = select(func.count()).select_from(Book)
            result = await session.execute(stmt)
            total_records = result.scalar()

            total_pages = ceil(total_records / limit) if total_records > 0 else 1

            stmt = select(Book).offset((page - 1) * limit).limit(limit)
            result = await session.execute(stmt)
            books = result.scalars().all()

            return PaginatedBooksResponse(
                data=books,
                page=page,
                limit=limit,
                total_pages=total_pages,
                total_records=total_records,
            )

    async def update_object(self, id: int, data: dict) -> Book:
        """Обновляет данные книги по ID."""
        async with get_async_session() as session:
            stmt = update(Book).where(Book.book_id == id).values(data).returning(Book)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete_object(self, id: int) -> Book:
        """Удаляет книгу по ID."""
        async with get_async_session() as session:
            stmt = delete(Book).where(Book.book_id == id).returning(Book)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
