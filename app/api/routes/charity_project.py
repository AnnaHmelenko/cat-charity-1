from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_not_less_invested,
    check_name_duplicate,
    check_project_exists,
    check_project_not_closed,
    check_project_not_invested,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import distribute_investments

router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project_in.name, session)
    new_project = await charity_project_crud.create(project_in, session)
    sources = await donation_crud.get_not_fully_invested(session)
    changed = distribute_investments(target=new_project, sources=sources)
    session.add_all(changed)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch('/{project_id}', response_model=CharityProjectDB)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_not_closed(project)
    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)
        project.name = project_in.name
    if project_in.full_amount is not None:
        check_full_amount_not_less_invested(
            project, project_in.full_amount
        )
        project.full_amount = project_in.full_amount
        project.close_if_fully_invested()
    if project_in.description is not None:
        project.description = project_in.description
    await session.commit()
    await session.refresh(project)
    return project


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_not_invested(project)
    await session.delete(project)
    await session.commit()
    return project
