from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationFullDB, DonationShortDB, \
    DonationCreate
from app.services.investing import investing

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров. Получить список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True
)
async def create_donation(
        obj_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Для пользователей. Сделать пожертвование.
    """
    # @TODO: some validations before create
    created_donation = await donation_crud.create(obj_in, session, user)
    await investing(created_donation, session)
    await session.refresh(created_donation)
    return created_donation


@router.get(
    '/my',
    response_model=List[DonationShortDB],
    response_model_exclude={'user_id'}
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Получить список моих пожертвований."""
    my_donations = await donation_crud.get_by_user(
        user=user, session=session
    )
    return my_donations
