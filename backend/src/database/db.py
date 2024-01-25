from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

from src.config import settings
from src.database.base import Base

DB_URL = settings.DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from src.database.models.balance import UserBalance
    from src.database.models.user import User

    Base.metadata.create_all(bind=engine)

    User.balance = relationship("UserBalance", back_populates="user")
    UserBalance.user = relationship("User", back_populates="balance")


def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()
