"""
Модуль маршрутов для работы с авторами через API.

Предоставляет маршруты для выполнения CRUD-операций с авторами:
- (POST /create) Создание нового автора
- (GET /) Получение списка авторов с пагинацией
- (GET /{author_id}) Получение автора по ID
- (PUT /{author_id}) Обновление данных автора
- (DELETE /{author_id}) Удаление автора
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.routes.depens import author_controller, AuthorController
from src.schemas.author import (
    AuthorCreate,
    PaginatedAuthorsResponse,
    AuthorResponse,
    AuthorUpdate,
)

# Роутер для работы с авторами
router = APIRouter()


@router.post("/create", response_model=AuthorResponse)
async def create_author(
    author: AuthorCreate,
    controller: Annotated[AuthorController, Depends(author_controller)],
):
    """Создание нового автора."""
    return await controller.create_object(author)


@router.get("", response_model=PaginatedAuthorsResponse)
async def get_authors(
    controller: Annotated[AuthorController, Depends(author_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список авторов с пагинацией."""
    return await controller.read_objects(page, limit)


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    controller: Annotated[AuthorController, Depends(author_controller)],
):
    """Получает автора по ID."""
    return await controller.read_object(author_id)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author: AuthorUpdate,
    controller: Annotated[AuthorController, Depends(author_controller)],
):
    """Обновляет данные автора."""
    return await controller.update_object(author_id, author)


@router.delete("/{author_id}", response_model=AuthorResponse)
async def delete_author(
    author_id: int,
    controller: Annotated[AuthorController, Depends(author_controller)],
):
    """Удаляет автора."""
    return await controller.delete_object(author_id)
