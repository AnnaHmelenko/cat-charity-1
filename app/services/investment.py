from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def distribute_investments(
    new_obj,  # CharityProject или Donation
    session: AsyncSession,
):
    if isinstance(new_obj, CharityProject):
        donations = await donation_crud.get_not_fully_invested(session)
        for donation in donations:
            if new_obj.fully_invested:
                break
            donation_free = donation.full_amount - donation.invested_amount
            project_need = new_obj.full_amount - new_obj.invested_amount
            transfer = min(donation_free, project_need)
            donation.invested_amount += transfer
            new_obj.invested_amount += transfer
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
            if new_obj.invested_amount == new_obj.full_amount:
                new_obj.fully_invested = True
                new_obj.close_date = datetime.now()
    elif isinstance(new_obj, Donation):
        projects = await charity_project_crud.get_open_projects(session)
        for project in projects:
            if new_obj.fully_invested:
                break
            project_need = project.full_amount - project.invested_amount
            donation_free = new_obj.full_amount - new_obj.invested_amount
            transfer = min(project_need, donation_free)
            project.invested_amount += transfer
            new_obj.invested_amount += transfer
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            if new_obj.invested_amount == new_obj.full_amount:
                new_obj.fully_invested = True
                new_obj.close_date = datetime.now()
    await session.commit()
