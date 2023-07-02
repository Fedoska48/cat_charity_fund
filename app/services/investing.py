from datetime import datetime
from select import select
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProject, Donation]:
    """
    Процесс инвестирования.
    Увеличение invested_amount, как в проектах, так и в пожертвованиях.
    Установка значений fully_invested и close_date, при необходимости.
    """
    ...


async def get_not_invested_objects(
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    """Получить объекты, которые еще не полностью проинвестированы."""
    not_invested_objects = await session.execute(
        select(
            obj_in
        ).where(
            obj_in.fully_invested == False  # noqa
        ).order_by(
            obj_in.create_date
        )
    )
    return not_invested_objects.scalars().all()


async def close_fully_invested_object(
        obj_in: Union[CharityProject, Donation],
) -> None:
    """Закрывает объект инвестирования."""
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
