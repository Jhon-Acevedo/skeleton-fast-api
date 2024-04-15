from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from src.auth.service.services import get_token, get_refresh_token
from src.config.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        return await get_token(data=data, db=db)
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)
