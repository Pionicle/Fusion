"""
Модуль описывает структуру базы данных для управления библиотечной системой.

Основные сущности:
- Author - авторы книг.
- Book - книги.
- Reader - читатели.
- Book_Readers - связи между книгами и читателями (кто какие книги взял).

Связи между сущностями:
- Author может быть автором нескольких книг (один-ко-многим с `Book`).
- Book связана с одним автором (`author_id` может быть `NULL`).
- Reader может брать несколько книг, и одна книга может быть взята несколькими читателями (многие-ко-многим через `Book_Readers`).
- Book_Readers связывает книгу и читателя, фиксируя, кто взял какую книгу.
"""

import re
import enum
from typing import Optional
from contextlib import asynccontextmanager

from sqlalchemy import ForeignKey, Table, Column, Integer, String, Date
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    relationship,
    mapped_column,
    validates,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.dialects.postgresql import ENUM

from src.config import DATABASE_URL

# Создание асинхронного движка базы данных
engine = create_async_engine(DATABASE_URL)

# Конструктор для создания сессии подключения к базе данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_async_session():
    """
    Получение сессии для подключения к базе данных.
    """
    async with async_session_maker() as session:
        yield session


class Nationality(str, enum.Enum):
    russian = "Russian"
    american = "American"
    british = "British"
    french = "French"
    german = "German"


NationalityEnum = ENUM(
    Nationality.russian,
    Nationality.american,
    Nationality.british,
    Nationality.french,
    Nationality.german,
    name="nationality",
    create_type=True,
)


class BookCategory(str, enum.Enum):
    fiction = "Fiction"
    non_fiction = "Non-fiction"
    science = "Science"
    history = "History"
    fantasy = "Fantasy"


BookCategoryEnum = ENUM(
    BookCategory.fiction,
    BookCategory.non_fiction,
    BookCategory.science,
    BookCategory.history,
    BookCategory.fantasy,
    name="book_category",
    create_type=True,
)


class Base(DeclarativeBase):
    pass


book_readers = Table(
    "book_readers",
    Base.metadata,
    Column("book_id", ForeignKey("books.book_id"), primary_key=True),
    Column("reader_id", ForeignKey("readers.reader_id"), primary_key=True),
    info={
        "doc": """Таблица для связи книг и читателей.

        Содержит информацию о том, какие читатели взяли какие книги, представляя собой
        отношение многие-ко-многим между таблицами `books` и `readers`.

        Attributes:
            book_id (int): Идентификатор книги (внешний ключ, ссылается на `books.book_id`).
            reader_id (int): Идентификатор читателя (внешний ключ, ссылается на `readers.reader_id`).

        Constraints:
            - Первичный ключ: (book_id, reader_id).
            - Внешний ключ book_id с каскадным удалением.
            - Внешний ключ reader_id с каскадным удалением.
        """
    },
)


class Author(Base):
    """Таблица авторов книг.

    Содержит информацию об авторах, включая их имена и национальность.
    Каждый автор может быть связан с несколькими книгами.

    Attributes:
        author_id (int): Уникальный идентификатор автора (первичный ключ, автоинкремент).
        first_name (str): Имя автора (максимум 50 символов, не null).
        last_name (str): Фамилия автора (максимум 50 символов, не null).
        nationality (Nationality): Национальность автора (enum: Russian, American, British, French, German, не null).
        books (list[Book]): Список книг, написанных автором (один-ко-многим).

    Relationships:
        - Один ко многим с таблицей `books` через `author_id`.
    """

    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    nationality: Mapped[Nationality] = mapped_column(NationalityEnum, nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    """Таблица книг в библиотеке.

    Содержит информацию о книгах, включая название, год публикации, категорию и автора.
    Каждая книга может быть взята несколькими читателями.

    Attributes:
        book_id (int): Уникальный идентификатор книги (первичный ключ, автоинкремент).
        title (str): Название книги (максимум 50 символов, уникальное, не null).
        publication_year (Date): Год публикации книги (не null).
        category (BookCategory): Категория книги (enum: Fiction, Non-fiction, Science, History, Fantasy, не null).
        author_id (Optional[int]): Идентификатор автора (внешний ключ, ссылается на `authors.author_id`, может быть null).
        author (Author): Автор книги (связь один-к-одному).
        readers (list[Reader]): Список читателей, взявших книгу (многие-ко-многим через `book_readers`).

    Relationships:
        - Один ко многим с таблицей `authors` через `author_id`.
        - Многие ко многим с таблицей `readers` через `book_readers`.
    """

    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    publication_year: Mapped[Date] = mapped_column(Date, nullable=False)
    category: Mapped[BookCategory] = mapped_column(BookCategoryEnum, nullable=False)
    author_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
    readers: Mapped[list["Reader"]] = relationship(
        "Reader", secondary=book_readers, back_populates="books"
    )


class Reader(Base):
    """Таблица читателей библиотеки.

    Содержит информацию о читателях, включая их имена и email.
    Каждый читатель может взять несколько книг.

    Attributes:
        reader_id (int): Уникальный идентификатор читателя (первичный ключ, автоинкремент).
        first_name (str): Имя читателя (максимум 50 символов, не null).
        last_name (str): Фамилия читателя (максимум 50 символов, не null).
        email (str): Email читателя (максимум 255 символов, уникальный, не null, с проверкой формата).
        books (list[Book]): Список книг, взятых читателем (многие-ко-многим через `book_readers`).

    Relationships:
        - Многие ко многим с таблицей `books` через `book_readers`.

    Methods:
        validate_email: Проверяет корректность формата email.
    """

    __tablename__ = "readers"

    reader_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    books: Mapped[list["Book"]] = relationship(
        secondary=book_readers, back_populates="readers"
    )

    @validates("email")
    def validate_email(self, key, email: str):
        """Проверяет корректность формата email.

        Args:
            key (str): Название поля (email).
            email (str): Значение email для проверки.

        Returns:
            str: Проверенное значение email.

        Raises:
            ValueError: Если email не соответствует формату.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if email and not re.match(pattern, email):
            raise ValueError("Invalid email address")
        return email
