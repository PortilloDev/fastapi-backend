from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from fastapi import Depends


router = APIRouter(
    tags=["Login"],
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool


class UserDB(User):
    password: str


    
users_db = {
    "ivan": {"id": 1, "username": "ivan", "email": "john@example.com", "active": True, "password": "password"},
    "alicia": {"id": 2, "username": "alicia", "email": "jane@example.com", "active": False, "password": "password"},
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




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    user = search_user_db(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(user: User = Depends(get_current_user)):
    return user