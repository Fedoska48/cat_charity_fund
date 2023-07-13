from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_id_by_name(
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        """Получить ID проекта по названию."""
        db_project_id = await session.execute(
            select(
                CharityProject.id
            ).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    @staticmethod
    async def get_project_status_by_id(
            project_id: int,
            session: AsyncSession
    ) -> None:
        """Получить статус проект по ID."""
        db_project_status = await session.execute(
            select(
                CharityProject.fully_invested
            ).where(
                CharityProject.id == project_id
            )
        )
        db_project_status = db_project_status.scalars().first()
        return db_project_status


charity_project_crud = CRUDCharityProject(CharityProject)
