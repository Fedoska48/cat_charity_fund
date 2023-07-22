from datetime import datetime
from typing import Union, List

from sqlalchemy import select
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
    model_for_invest = (
        CharityProject if isinstance(obj_in, Donation) else Donation
    )
    not_invested_objects = await get_not_invested_objects(
        model_for_invest, session
    )
    if not_invested_objects:
        available = obj_in.full_amount
        for open_object in not_invested_objects:
            needs_amount = (open_object.full_amount -
                            open_object.invested_amount)
            ready_for_invest = (
                obj_in.full_amount
                if needs_amount > obj_in.full_amount
                else needs_amount
            )
            available -= ready_for_invest
            open_object.invested_amount += ready_for_invest
            obj_in.invested_amount += ready_for_invest

            if open_object.invested_amount == open_object.full_amount:
                await close_fully_invested_object(open_object)

            if not available:
                await close_fully_invested_object(obj_in)
                break
        await session.commit()
    return obj_in


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
    """Закрыть объект инвестирования."""
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
