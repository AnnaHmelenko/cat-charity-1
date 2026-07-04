from sqlalchemy import Column, Integer, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    __tablename__ = 'donation'

    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
