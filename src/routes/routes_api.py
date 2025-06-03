"""
Модуль маршрутов API приложения.
"""

from fastapi import APIRouter

from src.routes.api.author import router as author_router
from src.routes.api.book import router as book_router

# Создание основного роутера с префиксом /v1
router = APIRouter(prefix="/v1")


# Добавление роутера авторов под префиксом /authors с тегом "Authors"
router.include_router(author_router, prefix="/authors", tags=["Авторы"])

# Добавление роутера книг под префиксом /books с тегом "Books"
router.include_router(book_router, prefix="/books", tags=["Книги"])
