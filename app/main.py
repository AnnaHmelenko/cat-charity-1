from fastapi import FastAPI

from app.api.routes import charity_project, donation
from app.core.config import settings
from app.core.db import Base, engine

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
