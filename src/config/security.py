from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

from fastapi import Depends

from src.config.config import get_settings
from src.config.database import get_db
from src.users.model.user import User

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(get_db())

    user = db.query(User).filter(User.id == user_id).first()
    return user


class JWTAuth:

    @staticmethod
    async def authenticate(conn):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()

        if 'authorization' not in conn.headers:
            return guest

        token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
        if not token:
            return guest

        user = get_current_user(token=token)

        if not user:
            return guest

        return AuthCredentials('authenticated'), user
