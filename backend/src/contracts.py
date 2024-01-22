from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def email_password(cls, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            email = email_info.normalized.lower()
        except EmailNotValidError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
        return email

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be at least 6 characters long"
            )
        if not any(char.isalpha() for char in value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must contain at least one letter"
            )
        if not any(char.isdigit() for char in value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must contain at least one digit"
            )
        return value


class User(UserCreate):
    id: int
