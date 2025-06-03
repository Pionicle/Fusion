"""
Модуль для создания зависимостей.
"""

from src.controllers.author import AuthorController
from src.controllers.book import BookController
from src.controllers.reader import ReaderController


def author_controller() -> AuthorController:
    """Возвращает новый экземпляр AuthorController."""
    return AuthorController()


def book_controller() -> BookController:
    """Возвращает новый экземпляр BookController."""
    return BookController()


def reader_controller() -> ReaderController:
    """Возвращает новый экземпляр ReaderController."""
    return ReaderController()
