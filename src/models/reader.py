"""
Модуль ReaderModel реализует модель для работы с читателями в базе данных.
Наследуется от BaseModel и обеспечивает CRUD-операции с использованием SQLAlchemy.
"""

from sqlalchemy import insert, select, update, delete, func
from math import ceil

from sqlalchemy.orm import selectinload

from src.models.abc_model import BaseModel
from src.database import get_async_session, Reader, book_readers
from src.schemas.reader import PaginatedReadersResponse


class ReaderModel(BaseModel):
    """Модель для работы с читателями в базе данных через CRUD-операции."""

    async def create_object(self, data: dict) -> Reader:
        """Создаёт нового читателя в базе данных."""
        async with get_async_session() as session:
            stmt = insert(Reader).values(data).returning(Reader)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def read_object(self, id: int) -> Reader:
        """Получает читателя по ID."""
        async with get_async_session() as session:
            stmt = (
                select(Reader)
                .where(Reader.reader_id == id)
                .options(selectinload(Reader.books))
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def read_objects(self, page: int, limit: int) -> PaginatedReadersResponse:
        """Получает список читателей с пагинацией."""
        async with get_async_session() as session:
            stmt = select(func.count()).select_from(Reader)
            result = await session.execute(stmt)
            total_records = result.scalar()

            total_pages = ceil(total_records / limit) if total_records > 0 else 1

            stmt = select(Reader).offset((page - 1) * limit).limit(limit)
            result = await session.execute(stmt)
            readers = result.scalars().all()

            return PaginatedReadersResponse(
                data=readers,
                page=page,
                limit=limit,
                total_pages=total_pages,
                total_records=total_records,
            )

    async def update_object(self, id: int, data: dict) -> Reader:
        """Обновляет данные читателя по ID."""
        async with get_async_session() as session:
            stmt = (
                update(Reader)
                .where(Reader.reader_id == id)
                .values(data)
                .options(selectinload(Reader.books))
                .returning(Reader)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete_object(self, id: int) -> Reader:
        """Удаляет читателя по ID."""
        async with get_async_session() as session:
            stmt = delete(Reader).where(Reader.reader_id == id).returning(Reader)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def add_book_to_reader(self, reader_id: int, book_id: int) -> Reader:
        """Добавляет книгу к читателю."""
        async with get_async_session() as session:
            stmt = insert(book_readers).values(book_id=book_id, reader_id=reader_id)
            result = await session.execute(stmt)
            await session.commit()

            stmt = (
                select(Reader)
                .where(Reader.reader_id == reader_id)
                .options(selectinload(Reader.books))
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def remove_book_from_reader(self, reader_id: int, book_id: int) -> Reader:
        """Удаляет книгу от читателя."""
        async with get_async_session() as session:
            stmt = delete(book_readers).where(
                book_readers.c.book_id == book_id, book_readers.c.reader_id == reader_id
            )
            result = await session.execute(stmt)
            await session.commit()

            stmt = (
                select(Reader)
                .where(Reader.reader_id == reader_id)
                .options(selectinload(Reader.books))
            )
            result = await session.execute(stmt)
            return result.scalar_one()
