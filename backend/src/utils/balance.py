from fastapi import HTTPException, status

from src.database.db import get_db
from src.database.models.balance import UserBalance
from src.database.models.user import User


def get_user_balance(current_user: User):
    with get_db() as db:
        user_balance = db.query(UserBalance.balance).filter(UserBalance.user_id == current_user.id).first()
    if user_balance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User balance not found")

    return user_balance.balance


def make_deposit(current_user: User, amount: float):
    with get_db() as db:
        balance = get_user_balance(current_user)
        new_balance = balance + amount
        db.query(UserBalance).filter(UserBalance.user_id == current_user.id).update({"balance": new_balance})
        db.commit()

    return new_balance


def make_withdrawal(current_user: User, amount: float):
    with get_db() as db:
        balance = get_user_balance(current_user)

    if amount > balance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    new_balance = balance - amount
    db.query(UserBalance).filter(UserBalance.user_id == current_user.id).update({"balance": new_balance})
    db.commit()

    return new_balance
