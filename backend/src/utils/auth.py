from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings
from src.database.db import get_db
from src.database.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Генерация JWT токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Генерация Refresh Token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Генерация JWT токена и Refresh Token
def create_tokens(data: dict) -> tuple[str, str]:
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token


# Получение текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme)) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


# Получение текущего пользователя из Refresh Токена
def get_current_user_refresh(token: str = Depends(oauth2_scheme)) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


# Регистрация пользователя
def register_user(email: str, password: str) -> User:
    hashed_password = pwd_context.hash(password)
    db_user = User(email=email, password=hashed_password)
    db = get_db()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Получение пользователя по email
def get_user_by_email(email: str) -> User | None:
    db = get_db()
    return db.query(User).filter(User.email == email).first()


# Аутентификация пользователя
def authenticate_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if user and pwd_context.verify(password, user.password):
        return user
    return None
