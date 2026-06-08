"""
Базовый класс для ORM-моделей.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Все модели наследуются от этого класса."""
    pass
