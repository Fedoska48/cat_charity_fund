from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    @staticmethod
    async def get_by_user(
            user: User,
            session: AsyncSession
    ):
        """Получить список донатов по пользователю."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
