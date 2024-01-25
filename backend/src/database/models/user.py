from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class User(Base):
    __tablename__ = "user_credentials"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    balance = relationship("UserBalance", back_populates="user")
    tasks = relationship("UserTask", back_populates="user")
