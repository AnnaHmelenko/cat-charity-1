from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.services.investment import distribute_investments
from app.validators import (
    check_project_exists,
    check_project_not_closed,
    check_project_not_invested,
)

router = APIRouter()


@router.post("/", response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_project = await charity_project_crud.create(project_in, session, commit=False)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует"
        )
    sources = await donation_crud.get_not_fully_invested(session)
    distribute_investments(target=new_project, sources=sources)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get("/", response_model=list[CharityProjectDB])
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch("/{project_id}", response_model=CharityProjectDB)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_not_closed(project)

    if project_in.full_amount is not None:
        if project_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя установить сумму сбора меньше уже вложенной"
            )
        project.full_amount = project_in.full_amount
        if project_in.full_amount <= project.invested_amount:
            project.close_project()

    if project_in.name is not None:
        # Проверка уникальности через IntegrityError при коммите
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description

    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует"
        )
    await session.refresh(project)
    return project


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    check_project_not_invested(project)
    await session.delete(project)
    await session.commit()
    return project
