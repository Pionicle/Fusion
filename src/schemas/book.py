"""
Модуль со схемами для валидации класса Book.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import date as Date


class BookCategory(str, Enum):
    """Enum для указания категории книги."""

    FICTION = "Fiction"
    NON_FICTION = "Non-fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    FANTASY = "Fantasy"


class BookResponse(BaseModel):
    """Схема для представления книги."""

    model_config = {"from_attributes": True}
    book_id: int = Field(..., description="Unique identifier of the book")
    title: str = Field(..., max_length=50, description="Book title", unique=True)
    publication_year: Date = Field(..., description="Publication year of the book")
    category: BookCategory = Field(..., description="Category of the book")
    author_id: Optional[int] = Field(None, description="Identifier of the author")


class PaginatedBooksResponse(BaseModel):
    """Схема для представления списка книг с пагинацией."""

    model_config = {"from_attributes": True}
    data: List[BookResponse] = Field(..., description="List of books")
    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Number of records per page")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    total_records: int = Field(..., ge=0, description="Total number of records")


class BookCreate(BaseModel):
    """Схема для представления данных книги при создании."""

    title: str = Field(..., max_length=50, description="Book title", unique=True)
    publication_year: Date = Field(..., description="Publication year of the book")
    category: BookCategory = Field(..., description="Category of the book")
    author_id: Optional[int] = Field(None, description="Identifier of the author")


class BookUpdate(BaseModel):
    """Схема для представления данных книги при обновлении."""

    title: Optional[str] = Field(None, max_length=50, description="Book's title")
    publication_year: Optional[Date] = Field(
        None, description="Publication year of the book"
    )
    category: Optional[BookCategory] = Field(None, description="Book category")
    author_id: Optional[int] = Field(None, description="Identifier of the author")
