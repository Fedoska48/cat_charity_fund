from sqlalchemy.ext.asyncio import AsyncSession


async def investing(
        obj_in,
        session: AsyncSession
):
    """
    Процесс инвестирования.
    Увеличение invested_amount, как в проектах, так и в пожертвованиях.
    Установка значений fully_invested и close_date, при необходимости.
    """