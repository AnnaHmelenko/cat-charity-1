from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        return (
            await session.execute(
                select(self.model).where(self.model.id == obj_id)
            )
        ).scalar_one_or_none()

    async def get_multi(self, session: AsyncSession):
        return (
            await session.execute(select(self.model))
        ).scalars().all()

    async def create(self, obj_in, session: AsyncSession):
        db_obj = self.model(**obj_in.dict())
        session.add(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        return db_obj

    async def get_not_fully_invested(self, session: AsyncSession):
        return (
            await session.execute(
                select(self.model)
                .where(self.model.fully_invested.is_(False))
                .order_by(self.model.create_date)
            )
        ).scalars().all()
