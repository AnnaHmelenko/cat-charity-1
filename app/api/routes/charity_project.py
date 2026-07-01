from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB)
from app.services.investment import distribute_investments

router = APIRouter()


@router.post("/", response_model=CharityProjectDB)
async def create_charity_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_project = await charity_project_crud.create(project_in, session)
    except IntegrityError as e:
        if 'UNIQUE constraint failed: charityproject.name' in str(e):
            raise HTTPException(
                status_code=400, detail="Проект с таким именем уже существует")
        raise
    await distribute_investments(new_project, session)
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
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать")

    # Обработка full_amount
    if project_in.full_amount is not None:
        if project_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail="Нельзя установить сумму сбора меньше уже вложенной"
            )
        project.full_amount = project_in.full_amount
        # Если новая сумма <= уже вложенной, закрываем проект
        if project_in.full_amount <= project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()
            # Сохраняем изменения
            try:
                await session.commit()
            except IntegrityError as e:
                if 'UNIQUE constraint failed: charityproject.name' in str(e):
                    raise HTTPException(
                        status_code=400,
                        detail="Проект с таким именем уже существует")
                raise
            await session.refresh(project)
            return project

    # Обновляем остальные поля (если переданы)
    if project_in.name is not None:
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description

    try:
        await session.commit()
    except IntegrityError as e:
        if 'UNIQUE constraint failed: charityproject.name' in str(e):
            raise HTTPException(
                status_code=400, detail="Проект с таким именем уже существует")
        raise
    await session.refresh(project)
    return project


@router.delete("/{project_id}", response_model=CharityProjectDB)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить проект, в который уже инвестированы ср-ва")
    await session.delete(project)
    await session.commit()
    return project
