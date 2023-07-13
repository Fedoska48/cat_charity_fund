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
            status_code=422,
            detail='Переговорка с таким именем уже существует!'
        )
    return project_id


# TODO: func
async def check_new_full_amount_bigger_than_invested_amount():
    ...

# @TODO: error messages for constants
