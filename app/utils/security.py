from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dateutil.relativedelta import relativedelta
from app.repositories.users import UsersRepository
from app.db.models import Users
from app.dto.schemas import TokenData
from datetime import datetime
from jose import jwt, JWTError
from typing import Annotated

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
SECRET_KEY = "LOREMLOREMLOREM"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def validate_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_token(data: dict, expire_relativedelta: relativedelta = relativedelta(minutes=+30)):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + expire_relativedelta
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    repository = UsersRepository()
    credentials_exception = HTTPException(
        status_code="401",
        detail="Could not validate credentials",
        headers={ "WWW-AUTHENTICATE": "Bearer" }
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user: Users | None = repository.get_one_by(Users.email == token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[Users, Depends(get_current_user)]) -> Users:
    if current_user.status is False:
        raise HTTPException(
            status_code=403,
            detail="The user is deleted"
        )
    return current_user