from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)

    def close_project(self):
        self.fully_invested = True
        self.close_date = datetime.utcnow()

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
