from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationFullDB

router = APIRouter()


# @TODO get_all_donations

@router.get(
    '/',
    response_model=List[DonationFullDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations

# @TODO create_donation

# @TODO get_user_donations
