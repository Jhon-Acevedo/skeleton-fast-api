from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.config.security import oauth2_scheme
from src.users.controller.responses import UserResponse
from src.users.controller.schemas import CreateUserRequest
from src.users.service.services import create_user_account, get_user_by_id

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        await create_user_account(data=data, db=db)
        payload = {"message": "User account has been successfully created."}
        return JSONResponse(content=payload)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    print(str(request.body()))
    return request.user


@user_router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def user_by_id(user_id, db: Session = Depends(get_db)):
    return await get_user_by_id(user_id=user_id, db=db)
