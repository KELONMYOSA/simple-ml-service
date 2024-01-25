from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class CeleryTask(Base):
    __tablename__ = "celery_tasks"

    id = Column(Integer, primary_key=True, index=True)
    celery_task = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    input_data = Column(JSON, nullable=False)
    prediction = Column(Boolean)
    task_result = Column(String, nullable=False)

    model = relationship("Model", back_populates="tasks")
    users = relationship("UserTask", back_populates="tasks")
