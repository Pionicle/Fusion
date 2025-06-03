"""
Модуль маршрутов для работы с читателями через API.

Предоставляет маршруты для выполнения CRUD-операций с читателями:
- (POST /create) Создание нового читателя
- (GET /) Получение списка читателей с пагинацией
- (GET /{reader_id}) Получение читателя по ID
- (PUT /{reader_id}) Обновление данных читателя
- (DELETE /{reader_id}) Удаление читателя
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.routes.depens import reader_controller, ReaderController
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
    reader: ReaderCreate,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Создаёт нового читателя."""
    return await controller.create_object(reader)


@router.get("", response_model=PaginatedReadersResponse)
async def get_readers(
    controller: Annotated[ReaderController, Depends(reader_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список читателей с пагинацией."""
    return await controller.read_objects(page, limit)


@router.get("/{reader_id}", response_model=ReaderResponse)
async def get_reader(
    reader_id: int,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Получает читателя по ID."""
    return await controller.read_object(reader_id)


@router.put("/{reader_id}", response_model=ReaderResponse)
async def update_reader(
    reader_id: int,
    reader: ReaderUpdate,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Обновляет данные читателя."""
    return await controller.update_object(reader_id, reader)


@router.delete("/{reader_id}", response_model=ReaderResponse)
async def delete_reader(
    reader_id: int,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Удаляет читателя."""
    return await controller.delete_object(reader_id)


@router.put("/{reader_id}/books/{book_id}", response_model=ReaderResponse)
async def add_book_to_reader(
    reader_id: int,
    book_id: int,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Добавляет книгу в список читателя."""
    return await controller.add_book_to_reader(reader_id, book_id)


@router.delete("/{reader_id}/books/{book_id}", response_model=ReaderResponse)
async def remove_book_from_reader(
    reader_id: int,
    book_id: int,
    controller: Annotated[ReaderController, Depends(reader_controller)],
):
    """Удаляет книгу из списка читателя."""
    return await controller.remove_book_from_reader(reader_id, book_id)
