from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def check_name_duplicate(name: str, session: AsyncSession):
    project = (
        await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
    ).scalars().first()
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует',
        )


async def check_project_exists(project_id: int, session: AsyncSession):
    project = (
        await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
    ).scalars().first()
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден',
        )
    return project


def check_project_not_closed(project):
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать',
        )


def check_project_not_invested(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить проект, в который уже вложены средства',
        )


def check_full_amount_not_less_invested(project, new_amount: int):
    if new_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить сумму сбора меньше уже вложенной',
        )
