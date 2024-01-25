from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)

    tasks = relationship("CeleryTask", back_populates="model")
