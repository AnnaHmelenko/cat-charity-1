from sqlalchemy import Column, String, Text, Integer
from app.models.base import BaseModel


class CharityProject(BaseModel):
    __tablename__ = "charityproject"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
