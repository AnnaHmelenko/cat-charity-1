from sqlalchemy import Column, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    comment = Column(Text, nullable=True)
