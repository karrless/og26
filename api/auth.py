from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

import config

router = APIRouter(prefix="/auth")
security = HTTPBearer()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    valid_user = data.username == config.API_USERNAME
    valid_password = valid_user and bcrypt.checkpw(
        data.password.encode(), config.API_PASSWORD_HASH.encode()
    )
    if not valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")

    payload = {
        "sub": data.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
    return LoginResponse(access_token=token)


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, config.JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")