from fastapi.exceptions import HTTPException
from datetime import datetime

from src.config.security import get_password_hash
from src.users.model.user import User


async def create_user_account(data, db):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def get_user_by_id(user_id, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found.")
