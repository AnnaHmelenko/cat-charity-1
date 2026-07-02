import datetime

from sqlalchemy import Column, Integer, Text, Boolean, DateTime

from app.core.db import Base


class Donation(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    close_date = Column(DateTime, nullable=True)
