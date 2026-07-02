from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    async def get_open_projects(self, session: AsyncSession):
        result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(False),
                CharityProject.invested_amount < CharityProject.full_amount
            ).order_by(CharityProject.create_date)
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
