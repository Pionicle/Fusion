"""
Модуль маршрутов для работы с читателями через API.

Предоставляет маршруты для выполнения CRUD-операций с читателями:
- (POST /create) Создание нового читателя
- (GET /) Получение списка читателей с пагинацией
- (GET /{reader_id}) Получение читателя по ID
- (PUT /{reader_id}) Обновление данных читателя
- (DELETE /{reader_id}) Удаление читателя
"""

import json
from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.routes.depens import (
    reader_controller,
    redis_client,
    ReaderController,
    RedisClient,
)
from src.schemas.reader import (
    ReaderResponse,
    PaginatedReadersResponse,
    ReaderCreate,
    ReaderUpdate,
)

# Роутер для работы с читателями
router = APIRouter()


@router.post("/create", response_model=ReaderResponse)
async def create_reader(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader: ReaderCreate,
):
    """Создаёт нового читателя."""
    return await controller.create_object(reader)


@router.get("", response_model=PaginatedReadersResponse)
async def get_readers(
    redis_client: Annotated[RedisClient, Depends(redis_client)],
    controller: Annotated[ReaderController, Depends(reader_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список читателей с пагинацией."""
    cache_key = f"readers:page:{page}:limit:{limit}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    readers = await controller.read_objects(page, limit)

    await redis_client.set(cache_key, readers.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return readers


@router.get("/{reader_id}", response_model=ReaderResponse)
async def get_reader(
    redis_client: Annotated[RedisClient, Depends(redis_client)],
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader_id: int,
):
    """Получает читателя по ID."""
    cache_key = f"reader:{reader_id}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    reader = await controller.read_object(reader_id)

    await redis_client.set(cache_key, reader.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return reader


@router.put("/{reader_id}", response_model=ReaderResponse)
async def update_reader(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader: ReaderUpdate,
    reader_id: int,
):
    """Обновляет данные читателя."""
    return await controller.update_object(reader_id, reader)


@router.delete("/{reader_id}", response_model=ReaderResponse)
async def delete_reader(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader_id: int,
):
    """Удаляет читателя."""
    return await controller.delete_object(reader_id)


@router.put("/{reader_id}/books/{book_id}", response_model=ReaderResponse)
async def add_book_to_reader(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader_id: int,
    book_id: int,
):
    """Добавляет книгу в список читателя."""
    return await controller.add_book_to_reader(reader_id, book_id)


@router.delete("/{reader_id}/books/{book_id}", response_model=ReaderResponse)
async def remove_book_from_reader(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    reader_id: int,
    book_id: int,
):
    """Удаляет книгу из списка читателя."""
    return await controller.remove_book_from_reader(reader_id, book_id)
