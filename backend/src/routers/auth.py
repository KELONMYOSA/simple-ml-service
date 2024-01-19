from backend.src.contracts import Token, UserReg
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/register", response_model=Token, tags=["Authorization"])
async def register(user: UserReg):
    return {"access_token": "Token", "token_type": "bearer"}
