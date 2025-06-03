"""
Модуль для обработки ошибок.
"""

from fastapi import HTTPException


from functools import wraps
import sqlalchemy.exc
from typing import Callable, TypeVar, Any

# Тип возвращаемого значения
T = TypeVar("T")


def handle_no_result_found(func: Callable[..., T]) -> Callable[..., T]:
    """
    Декоратор для обработки ситуации, когда нет результата.

    Raises:
        HTTPException: В случае отсутствия результата.

    Returns:
        Callable[..., T]: _description_
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=404, detail="Объект не найден.")

    return wrapper


def handle_integrity_error(func: Callable[..., T]) -> Callable[..., T]:
    """
    Декоратор для обработки ситуации запрещенной операции.

    Raises:
        HTTPException: В случае запрещенной операции.
    Returns:
        Callable[..., T]: _description_
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=409, detail="Запрещена операция.")

    return wrapper
