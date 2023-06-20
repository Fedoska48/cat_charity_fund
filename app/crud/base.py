"""Базовые операциии CRUD."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Для соблюдения стиля DRY, создаем базовый класс для CRUD-операций."""

    def __init__(self, model):
        """При инициализации класса присваивается модель
        и далее все операции производятся над моделью."""
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Абстрактный метод для получения списка объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
