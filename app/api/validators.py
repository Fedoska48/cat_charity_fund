"""Валидаторы."""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_exists(
        project_id: id,
        session: AsyncSession
) -> CharityProject:
    """Проверить, что проект существует."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден!'
        )
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверить название проекта на уникальность."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )
    return project_id


async def check_new_full_amount_bigger_than_invested_amount(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession
):
    """Проверить, что новая финальная сумма не ниже уже инвестированной."""
    invested_amount = await charity_project_crud.get_invested_amount_by_id(
        project_id, session
    )
    if invested_amount > new_full_amount:
        raise HTTPException(
            status_code=400,
            detail="Новая сумма меньше, чем уже проинвестировано в проект!"
        )
    return invested_amount


async def check_project_already_got_donation(
        project_id: int,
        session: AsyncSession
):
    """Проверить, что в проект хотя бы что-то инвестировано."""
    invested_amount = await charity_project_crud.get_invested_amount_by_id(
        project_id, session
    )
    if invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return invested_amount


async def check_project_is_closed(
        project_id: int,
        session: AsyncSession
):
    """Проверить закрыт ли проект."""
    project_status = await charity_project_crud.get_project_status_by_id(
        project_id, session
    )
    if project_status:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project_status

# @TODO: error messages for constants
