from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_exists, check_name_duplicate, \
    check_project_is_closed, check_project_already_got_donation, \
    check_new_full_amount_bigger_than_invested_amount
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import User
from app.schemas.charity_project import CharityProjectDB, CharityProjectCreate, \
    CharityProjectUpdate
from app.services.investing import investing

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
    """
    Доступно для всех. Получает список всех проектов.
    """
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров. Создает благотворительный проект."""
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    await investing(new_charity_project, session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
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
    await check_project_exists(project_id, session)
    await check_project_is_closed(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    # @TODO new_full_amount > invested_amount validation
    if obj_in.full_amount:
        await check_new_full_amount_bigger_than_invested_amount(
            project_id, obj_in.full_amount, session
        )
    charity_project = charity_project_crud.update(
        project_id,
        obj_in,
        session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
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
    await check_project_exists(project_id, session)
    await check_project_already_got_donation(
        project_id, session
    )
    charity_project = charity_project_crud.remove(project_id, session)
    return charity_project
