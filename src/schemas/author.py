"""
Модуль со схемами для работы с авторами.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class Nationality(str, Enum):
    """Enum для указания национальности автора."""

    RUSSIAN = "Russian"
    AMERICAN = "American"
    BRITISH = "British"
    FRENCH = "French"
    GERMAN = "German"


class AuthorResponse(BaseModel):
    """Схема для представления автора."""

    author_id: int = Field(..., description="Unique identifier of the author")
    first_name: str = Field(..., max_length=50, description="Author's first name")
    last_name: str = Field(..., max_length=50, description="Author's last name")
    nationality: Nationality = Field(..., description="Author's nationality")
    model_config = {"from_attributes": True}


class DeleteAuthorResponse(BaseModel):
    """Схема для представления результата удаления автора."""

    success: bool = Field(..., description="Indicates if the deletion was successful")
    message: str = Field(..., description="Description of the operation result")
    author_id: Optional[int] = Field(
        None, description="ID of the deleted author, if applicable"
    )


class AuthorCreate(BaseModel):
    """Схема для представления данных автора при создании."""

    first_name: str = Field(..., max_length=50, description="Author's first name")
    last_name: str = Field(..., max_length=50, description="Author's last name")
    nationality: Nationality = Field(..., description="Author's nationality")


class AuthorUpdate(BaseModel):
    """Схема для представления данных автора при обновлении."""

    first_name: Optional[str] = Field(
        None, max_length=50, description="Author's first name"
    )
    last_name: Optional[str] = Field(
        None, max_length=50, description="Author's last name"
    )
    nationality: Optional[Nationality] = Field(None, description="Author's nationality")


class PaginatedAuthorsResponse(BaseModel):
    """Схема для представления списка авторов с пагинацией."""

    data: List[AuthorResponse] = Field(..., description="List of authors")
    page: int = Field(..., ge=1, description="Current page number")
    limit: int = Field(..., ge=1, le=100, description="Records per page")
    total_pages: int = Field(..., ge=1, description="Total number of pages")
    total_records: int = Field(..., ge=0, description="Total number of records")
    model_config = {"from_attributes": True}
