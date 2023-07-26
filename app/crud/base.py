"""Базовые операциии CRUD."""
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


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

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Абстрактый класс для получения экземпляра объекта."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        db_obj = db_obj.scalars().first()
        return db_obj

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ):
        """Абстрактный метод для создания объекта."""
        new_obj_data = obj_in.dict()
        if user is not None:
            new_obj_data['user_id'] = user.id
        db_obj = self.model(**new_obj_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
            commit: bool = True
    ):
        """Абстрактный метод обновления данных."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Абстрактный метод для удаления объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_invested(
        self,
        session: AsyncSession,
    ):
        """
        Получить не проинвестированные объекты с сортировкой по дате создания.
        """
        not_invested_objects = await session.execute(
            select(
                self.model
            ).where(
                self.model.fully_invested == False  # noqa
            ).order_by(
                self.model.create_date
            )
        )
        return not_invested_objects.scalars().all()

    async def get_status_by_id(
            self,
            object_id: int,
            session: AsyncSession
    ) -> None:
        """Получить статус объекта по ID."""
        db_object_status = await session.execute(
            select(
                self.model.fully_invested
            ).where(
                self.model.id == object_id
            )
        )
        return db_object_status.scalars().first()

    async def get_invested_amount_by_id(
            self,
            object_id: int,
            session: AsyncSession
    ):
        invested_amount = await session.execute(
            select(
                self.model.invested_amount
            ).where(
                self.model.id == object_id
            )
        )
        return invested_amount.scalars().first()
