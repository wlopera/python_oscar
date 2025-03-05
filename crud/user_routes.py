from fastapi import APIRouter
from models.user_models import UserCreate, UserUpdate
from crud.user_crud import create_user, read_user, update_user, delete_user

router = APIRouter()


@router.post("/users/")
async def create_user_endpoint(user: UserCreate):
    return await create_user(user)


@router.get("/users/{username}")
async def read_user_endpoint(username: str):
    return await read_user(username)


@router.put("/users/{username}")
async def update_user_endpoint(username: str, user: UserUpdate):
    return await update_user(username, user)


@router.delete("/users/{username}")
async def delete_user_endpoint(username: str):
    return await delete_user(username)
