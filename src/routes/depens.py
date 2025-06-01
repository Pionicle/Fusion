"""
Модуль для создания зависимостей.
"""

from src.controllers.author import AuthorController


def author_controller() -> AuthorController:
    """Возвращает новый экземпляр AuthorController."""
    return AuthorController()
