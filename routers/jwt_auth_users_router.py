from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from fastapi import Depends
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt


# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)


pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool


class UserDB(User):
    password: str


    
users_db = {
    "ivan": {"id": 1, "username": "ivan", "email": "john@example.com", "active": True, "password": "$2a$12$K/mz/Twleh8cq65SuVznOOJniuQh4g036gs2zmLRuCOumPdvWf9xm"},
    "alicia": {"id": 2, "username": "alicia", "email": "jane@example.com", "active": False, "password": "$2a$12$K/mz/Twleh8cq65SuVznOOJniuQh4g036gs2zmLRuCOumPdvWf9xm"},
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if user.active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user




@router.post("/auth/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    user = search_user_db(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/user/me")
async def read_users_me(user: User = Depends(get_current_user)):
    return user