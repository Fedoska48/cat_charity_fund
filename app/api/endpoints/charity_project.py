from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectDB, CharityProjectCreate, \
    CharityProjectUpdate

router = APIRouter()


# @TODO add general roles

@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров. Создает благотворительный проект."""
    # @TODO: only superuser
    # @TODO check_name_duplicate(obj, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    # @TODO: only superuser
    # @TODO check_project_exists(project_id, session)

    charity_project = charity_project_crud.remove(project_id, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    # @TODO: only superuser
    # @TODO new_full_amount > full_amount validation
    # @TODO check_exists
    # @TODO if obj_in.name: check_name_duplicate
    charity_project = charity_project_crud.update(
        project_id,
        obj_in,
        session
    )
    return charity_project
