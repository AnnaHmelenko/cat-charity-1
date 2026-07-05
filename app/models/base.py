from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import declared_attr

from app.core.db import Base


class InvestmentBase(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        kwargs.setdefault('invested_amount', 0)
        kwargs.setdefault('fully_invested', False)
        super().__init__(**kwargs)

    def close_project(self):
        if self.invested_amount == self.full_amount:
            self.fully_invested = True
            self.close_date = datetime.utcnow()

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} id={self.id} '
            f'full_amount={self.full_amount} '
            f'invested_amount={self.invested_amount} '
            f'fully_invested={self.fully_invested} '
            f'create_date={self.create_date} '
            f'close_date={self.close_date}>'
        )
