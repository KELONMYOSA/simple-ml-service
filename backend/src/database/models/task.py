from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database.base import Base


class UserTask(Base):
    __tablename__ = "user_tasks"

    user_id = Column(Integer, ForeignKey("user_credentials.id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("celery_tasks.id"), primary_key=True)

    user = relationship("User", back_populates="tasks")
    tasks = relationship("CeleryTask", back_populates="users")
