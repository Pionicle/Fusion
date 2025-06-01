"""
Модуль AuthorModel реализует модель для работы с авторами в базе данных.
Наследуется от BaseModel и обеспечивает CRUD-операции с использованием SQLAlchemy.
"""

from sqlalchemy import insert, select, update, delete, func
from math import ceil

from src.models.abc_model import BaseModel
from src.database import get_async_session, Author
from src.schemas.author import PaginatedAuthorsResponse


class AuthorModel(BaseModel):
    """Модель для работы с авторами в базе данных через CRUD-операции."""

    async def create_object(self, data: dict) -> Author:
        """Создаёт нового автора в базе данных."""
        async with get_async_session() as session:
            stmt = insert(Author).values(data).returning(Author)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def read_object(self, id: int) -> Author:
        """Получает автора по ID."""
        async with get_async_session() as session:
            stmt = select(Author).where(Author.author_id == id)
            result = await session.execute(stmt)
            return result.scalar_one()

    async def read_objects(self, page: int, limit: int) -> PaginatedAuthorsResponse:
        """Получает список авторов с пагинацией."""
        async with get_async_session() as session:
            stmt = select(func.count()).select_from(Author)
            result = await session.execute(stmt)
            total_records = result.scalar()

            total_pages = ceil(total_records / limit) if total_records > 0 else 1

            stmt = select(Author).offset((page - 1) * limit).limit(limit)
            result = await session.execute(stmt)
            authors = result.scalars().all()

            return PaginatedAuthorsResponse(
                data=authors,
                page=page,
                limit=limit,
                total_pages=total_pages,
                total_records=total_records,
            )

    async def update_object(self, id: int, data: dict) -> Author:
        """Обновляет данные автора по ID."""
        async with get_async_session() as session:
            stmt = (
                update(Author)
                .where(Author.author_id == id)
                .values(data)
                .returning(Author)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete_object(self, id: int) -> Author:
        """Удаляет автора по ID."""
        async with get_async_session() as session:
            stmt = delete(Author).where(Author.author_id == id).returning(Author)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
