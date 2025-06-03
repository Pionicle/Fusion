"""
Модуль маршрутов для работы с книгами через API.

Предоставляет маршруты для выполнения CRUD-операций с книгами:
- (POST /create) Создание новой книги
- (GET /) Получение списка книг с пагинацией
- (GET /{book_id}) Получение книги по ID
- (PUT /{book_id}) Обновление данных книги
- (DELETE /{book_id}) Удаление книги
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.routes.depens import book_controller, BookController
from src.schemas.book import (
    BookCreate,
    PaginatedBooksResponse,
    BookResponse,
    BookUpdate,
)

# Роутер для работы с книгами
router = APIRouter()


@router.post("/create", response_model=BookResponse)
async def create_book(
    book: BookCreate,
    controller: Annotated[BookController, Depends(book_controller)],
):
    """Создание новой книги."""
    return await controller.create_object(book)


@router.get("", response_model=PaginatedBooksResponse)
async def get_books(
    controller: Annotated[BookController, Depends(book_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список книг с пагинацией."""
    return await controller.read_objects(page, limit)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    controller: Annotated[BookController, Depends(book_controller)],
):
    """Получает книгу по ID."""
    return await controller.read_object(book_id)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book: BookUpdate,
    controller: Annotated[BookController, Depends(book_controller)],
):
    """Обновляет данные книги."""
    return await controller.update_object(book_id, book)


@router.delete("/{book_id}", response_model=BookResponse)
async def delete_book(
    book_id: int,
    controller: Annotated[BookController, Depends(book_controller)],
):
    """Удаляет книгу."""
    return await controller.delete_object(book_id)
