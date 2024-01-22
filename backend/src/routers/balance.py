from fastapi import APIRouter, Depends

from src.contracts import User
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/balance",
    tags=["Account balance"],
)


# Пример защищенного эндпоинта
@router.get("/test", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
