from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.contracts import UserCreate
from src.utils.auth import authenticate_user, create_tokens, get_current_user, get_user_by_email, register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


# Регистрация пользователя
@router.post("/register")
def register(form_data: UserCreate = Depends()):
    user = get_user_by_email(form_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = register_user(form_data.email, form_data.password)

    return {"id": user.id, "email": user.email}


# Аутентификация пользователя и генерация токенов
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username.lower(), form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token, refresh_token = create_tokens({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


# Обновление токена с использованием Refresh Token
@router.post("/refresh")
def refresh(token: str):
    user = get_current_user(token, refresh=True)
    access_token, refresh_token = create_tokens({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
