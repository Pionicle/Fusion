"""
Модуль маршрутов для работы с книгами через API.

Предоставляет маршруты для выполнения CRUD-операций с книгами:
- (POST /create) Создание новой книги
- (GET /) Получение списка книг с пагинацией
- (GET /{book_id}) Получение книги по ID
- (PUT /{book_id}) Обновление данных книги
- (DELETE /{book_id}) Удаление книги
"""

import json
from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.routes.depens import (
    book_controller,
    redis_client,
    BookController,
    RedisClient,
)
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
    controller: Annotated[BookController, Depends(book_controller)],
    book: BookCreate,
):
    """Создание новой книги."""
    return await controller.create_object(book)


@router.get("", response_model=PaginatedBooksResponse)
async def get_books(
    redis_client: Annotated[RedisClient, Depends(redis_client)],
    controller: Annotated[BookController, Depends(book_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список книг с пагинацией."""
    cache_key = f"books:page:{page}:limit:{limit}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    books = await controller.read_objects(page, limit)

    await redis_client.set(cache_key, books.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return books


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    controller: Annotated[BookController, Depends(book_controller)],
    book_id: int,
):
    """Получает книгу по ID."""
    cache_key = f"book:{book_id}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    book = await controller.read_object(book_id)

    await redis_client.set(cache_key, book.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    controller: Annotated[BookController, Depends(book_controller)],
    book: BookUpdate,
    book_id: int,
):
    """Обновляет данные книги."""
    return await controller.update_object(book_id, book)


@router.delete("/{book_id}", response_model=BookResponse)
async def delete_book(
    controller: Annotated[BookController, Depends(book_controller)],
    book_id: int,
):
    """Удаляет книгу."""
    return await controller.delete_object(book_id)
