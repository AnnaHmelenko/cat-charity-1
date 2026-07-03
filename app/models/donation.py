from sqlalchemy import Column, Text, Integer
from app.models.base import BaseModel


class Donation(BaseModel):
    __tablename__ = "donation"

    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
