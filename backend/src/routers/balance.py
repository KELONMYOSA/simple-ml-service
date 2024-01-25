from fastapi import APIRouter, Depends, HTTPException, status

from src.database.models.user import User
from src.utils.auth import get_current_user
from src.utils.balance import get_user_balance, make_deposit, make_withdrawal

router = APIRouter(
    prefix="/balance",
    tags=["Account balance"],
)


# Метод для получения баланса пользователя
@router.get("/")
def get_balance(current_user: User = Depends(get_current_user)):
    balance = get_user_balance(current_user)
    return {"balance": balance}


# Метод для пополнения баланса
@router.post("/deposit")
def deposit_amount(amount: float, current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Deposit amount must be greater than 0")

    new_balance = make_deposit(current_user, amount)

    return {"balance": new_balance}


# Метод для списания с баланса
@router.post("/withdraw")
def withdraw_amount(amount: float, current_user: User = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Withdrawal amount must be greater than 0")

    new_balance = make_withdrawal(current_user, amount)

    return {"balance": new_balance}
