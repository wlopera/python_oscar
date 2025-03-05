from fastapi import HTTPException
from models.user_models import UserCreate, UserUpdate
from db.connection import db

# Accede a la colección 'users' desde la base de datos
collection = db["users"]


async def create_user(user: UserCreate):
    user.username = user.username.lower()
    if await collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}


async def read_user(username: str):
    user = await collection.find_one({"username": username.lower()}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return user


async def update_user(username: str, user: UserUpdate):
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    result = await collection.update_one({"username": username.lower()}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario actualizado satisfactoriamente"}


async def delete_user(username: str):
    result = await collection.delete_one({"username": username.lower()})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "usuario borrado satisfactoriamente"}
