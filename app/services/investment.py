from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def _invest_donations_into_project(new_project, session: AsyncSession):
    donations = await donation_crud.get_not_fully_invested(session)
    for donation in donations:
        if new_project.fully_invested:
            break
        donation_free = donation.full_amount - donation.invested_amount
        project_need = new_project.full_amount - new_project.invested_amount
        transfer = min(donation_free, project_need)
        donation.invested_amount += transfer
        new_project.invested_amount += transfer
        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
        if new_project.invested_amount == new_project.full_amount:
            new_project.fully_invested = True
            new_project.close_date = datetime.now()


async def _invest_project_into_donation(new_donation, session: AsyncSession):
    projects = await charity_project_crud.get_open_projects(session)
    for project in projects:
        if new_donation.fully_invested:
            break
        project_need = project.full_amount - project.invested_amount
        donation_free = new_donation.full_amount - new_donation.invested_amount
        transfer = min(project_need, donation_free)
        project.invested_amount += transfer
        new_donation.invested_amount += transfer
        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
        if new_donation.invested_amount == new_donation.full_amount:
            new_donation.fully_invested = True
            new_donation.close_date = datetime.now()


async def distribute_investments(new_obj, session: AsyncSession):
    if isinstance(new_obj, CharityProject):
        await _invest_donations_into_project(new_obj, session)
    elif isinstance(new_obj, Donation):
        await _invest_project_into_donation(new_obj, session)
    await session.commit()
