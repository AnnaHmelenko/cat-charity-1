from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj_in, session: AsyncSession, commit: bool = True):
        db_obj = self.model(**obj_in.dict())
        db_obj.invested_amount = 0
        db_obj.fully_invested = False
        session.add(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession, commit: bool = True):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_not_fully_invested(self, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False),
                self.model.invested_amount < self.model.full_amount
            ).order_by(self.model.create_date)
        )
        return result.scalars().all()
