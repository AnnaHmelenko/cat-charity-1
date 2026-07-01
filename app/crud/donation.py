from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.donation import Donation
from app.crud.base import CRUDBase


class CRUDDonation(CRUDBase):
    async def get_not_fully_invested(self, session: AsyncSession):
        result = await session.execute(
            select(Donation).where(
                Donation.fully_invested.is_(False),  # исправлено
                Donation.invested_amount < Donation.full_amount
            ).order_by(Donation.create_date)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
