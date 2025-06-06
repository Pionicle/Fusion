"""
Модуль маршрутов для работы с авторами через API.

Предоставляет маршруты для выполнения CRUD-операций с авторами:
- (POST /create) Создание нового автора
- (GET /) Получение списка авторов с пагинацией
- (GET /{author_id}) Получение автора по ID
- (PUT /{author_id}) Обновление данных автора
- (DELETE /{author_id}) Удаление автора
"""

import json
from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.routes.depens import (
    author_controller,
    redis_client,
    AuthorController,
    RedisClient,
)
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
    controller: Annotated[AuthorController, Depends(author_controller)],
    author: AuthorCreate,
):
    """Создание нового автора."""
    return await controller.create_object(author)


@router.get("", response_model=PaginatedAuthorsResponse)
async def get_authors(
    redis_client: Annotated[RedisClient, Depends(redis_client)],
    controller: Annotated[AuthorController, Depends(author_controller)],
    page: int = Query(1, ge=1, description="Номер страницы, начиная с 1"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
):
    """Получает список авторов с пагинацией."""
    cache_key = f"authors:page:{page}:limit:{limit}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    authors = await controller.read_objects(page, limit)

    await redis_client.set(cache_key, authors.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    redis_client: Annotated[RedisClient, Depends(redis_client)],
    controller: Annotated[AuthorController, Depends(author_controller)],
    author_id: int,
):
    """Получает автора по ID."""
    cache_key = f"author:{author_id}"
    cache_value = await redis_client.get(cache_key)
    if cache_value:
        return json.loads(cache_value)

    author = await controller.read_object(author_id)

    await redis_client.set(cache_key, author.model_dump_json())
    await redis_client.expire(cache_key, 15)

    return author


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    controller: Annotated[AuthorController, Depends(author_controller)],
    author: AuthorUpdate,
    author_id: int,
):
    """Обновляет данные автора."""
    return await controller.update_object(author_id, author)


@router.delete("/{author_id}", response_model=AuthorResponse)
async def delete_author(
    controller: Annotated[AuthorController, Depends(author_controller)],
    author_id: int,
):
    """Удаляет автора."""
    return await controller.delete_object(author_id)
