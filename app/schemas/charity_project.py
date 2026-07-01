from pydantic import BaseModel, Field, Extra
from datetime import datetime
from typing import Optional


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    class Config:
        extra = Extra.forbid   # запрещаем лишние поля


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid   # запрещаем лишние поля


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        from_attributes = True
