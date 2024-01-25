from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database.base import Base


class UserBalance(Base):
    __tablename__ = "user_balance"

    user_id = Column(Integer, ForeignKey("user_credentials.id"), primary_key=True, index=True)
    balance = Column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="balance")
