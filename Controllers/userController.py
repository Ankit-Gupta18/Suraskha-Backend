# Controllers/userController.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    # Logic to fetch users
    return {"message": "Users fetched successfully"}

@router.post("/users")
async def create_user(user_data: dict):
    # Logic to create a new user
    return {"message": "User created successfully"}
