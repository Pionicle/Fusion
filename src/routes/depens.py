"""
Модуль для создания зависимостей.
"""

from src.controllers.author import AuthorController
from src.controllers.book import BookController


def author_controller() -> AuthorController:
    """Возвращает новый экземпляр AuthorController."""
    return AuthorController()


def book_controller() -> BookController:
    """Возвращает новый экземпляр BookController."""
    return BookController()
