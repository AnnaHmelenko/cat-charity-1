from fastapi import FastAPI

from app.api.routes import charity_project, donation
from app.core.config import settings

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(
    charity_project.router,
    prefix='/charity_project',
    tags=['Проекты'],
)
app.include_router(
    donation.router,
    prefix='/donation',
    tags=['Пожертвования'],
)
