# api/book_routes.py
from fastapi import APIRouter, HTTPException
from models.user import User
from repositories.user_repository import UserRepository

router = APIRouter()

@router.get("/api/v1/users/")
async def get_users():
    return UserRepository.get_all_users()

@router.get("/api/v1/users/{user_id}")
async def get_user(user_id: int):
    user = UserRepository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/api/v1/users/")
async def create_user(user: User):
    UserRepository.add_user(user)
    return {"id": user.id}

@router.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: int):
    user = UserRepository.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
