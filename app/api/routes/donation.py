from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationCreateResponse,
    DonationDB,
)
from app.services.investment import distribute_investments

router = APIRouter()


@router.post('/', response_model=DonationCreateResponse)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation_in, session)
    sources = await charity_project_crud.get_not_fully_invested(session)
    changed = distribute_investments(target=new_donation, sources=sources)
    session.add_all(changed)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/', response_model=list[DonationDB])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)
