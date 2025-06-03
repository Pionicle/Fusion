"""
Модуль со схемами для валидации класса Reader.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class ReaderResponse(BaseModel):
    """Схема для представления читателя."""

    model_config = {"from_attributes": True}
    reader_id: int = Field(..., description="Unique identifier of the reader")
    first_name: str = Field(
        ..., max_length=50, description="Reader's name", nullable=False
    )
    last_name: str = Field(
        ..., max_length=50, description="Reader's surname", nullable=False
    )
    email: str = Field(..., max_length=255, description="Email of the reader")
    books: List["BookResponse"] = Field(
        ..., description="List of books borrowed by the reader"
    )


class ReaderSimpleResponse(BaseModel):
    """Схема для представления читателя."""

    model_config = {"from_attributes": True}
    reader_id: int = Field(..., description="Unique identifier of the reader")
    first_name: str = Field(
        ..., max_length=50, description="Reader's name", nullable=False
    )
    last_name: str = Field(
        ..., max_length=50, description="Reader's surname", nullable=False
    )
    email: str = Field(..., max_length=255, description="Email of the reader")


class PaginatedReadersResponse(BaseModel):
    """Схема для представления списка читателей с пагинацией."""

    model_config = {"from_attributes": True}
    data: List[ReaderSimpleResponse] = Field(..., description="List of readers")
    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Number of records per page")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    total_records: int = Field(..., ge=0, description="Total number of records")


class ReaderCreate(BaseModel):
    """Схема для представления данных читателя при создании."""

    first_name: str = Field(
        ..., max_length=50, description="Reader's name", nullable=False
    )
    last_name: str = Field(
        ..., max_length=50, description="Reader's surname", nullable=False
    )
    email: EmailStr = Field(..., max_length=255, description="Email of the reader")


class ReaderUpdate(BaseModel):
    """Схема для представления данных читателя при обновлении."""

    first_name: Optional[str] = Field(None, max_length=50, description="Reader's name")
    last_name: Optional[str] = Field(
        None, max_length=50, description="Reader's surname"
    )
    email: Optional[EmailStr] = Field(
        None, max_length=255, description="Email of the reader"
    )


from src.schemas.book import BookResponse  # noqa

ReaderResponse.model_rebuild()
