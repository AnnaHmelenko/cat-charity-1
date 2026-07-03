from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from http import HTTPStatus
from app.models.charity_project import CharityProject


async def check_project_exists(project_id: int, session: AsyncSession):
    result = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден"
        )
    return project


def check_project_not_closed(project):
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать"
        )


def check_project_not_invested(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя удалить проект, в который уже инвестированы средства"
        )
