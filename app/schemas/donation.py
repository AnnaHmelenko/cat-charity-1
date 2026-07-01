from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DonationBase(BaseModel):
    comment: Optional[str] = None
    full_amount: int = Field(..., gt=0)


class DonationCreate(DonationBase):
    pass


class DonationCreateResponse(BaseModel):
    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        from_attributes = True


class DonationDB(DonationCreateResponse):
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime]
