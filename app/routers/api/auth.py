from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.services.service import get_service
from app.dto.schemas import LogInOut
from app.dto.schemas import UsersIn
from app.utils.security import create_token

r = APIRouter(
    tags=["Authentication"],
    prefix="/api"
)

auth_service = lambda : get_service("auth")
users_service = lambda : get_service("users")

@r.post("/auth/users")
def create_user(user: UsersIn, response: Response, service=Depends(users_service)):
    result: bool = service.create(user)
    if result is False:
        raise HTTPException(400, "The user already exits")
    response.status_code = 201
    return { "message": "User created" }

@r.post("/token")
def login(login: OAuth2PasswordRequestForm = Depends(), service=Depends(auth_service)):
    email: str | None = service.login(login.username, login.password)
    if email is None:
        raise HTTPException(401, "The user doesn't exits or the password is invalid")
    data: dict = {
        "sub": email
    }
    access_token = create_token(data)
    return LogInOut(
        access_token=access_token,
        type="bearer"
    )