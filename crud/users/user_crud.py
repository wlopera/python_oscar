from fastapi import HTTPException
from models.user_models import UserCreate, UserUpdate
from db.connection import get_db_user


"""
    Crear usuario:
        - Obtener la conexion DB
        - Validar si el usuario no existe (nuevo)
        - Insertar usuario en MongoDB Atlas
"""
async def create_user(user: UserCreate):
    collection = await get_db_user()  # Obtener conexión en cada petición
    user.username = user.username.lower()
    if await collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}


"""
    Concultar usuario:
        - Obtener la conexion DB
        - Buscar usuario en MongoDB Atalas
"""
async def read_user(username: str):
    collection = await get_db_user()  # Obtener conexión en cada petición
    user = await collection.find_one({"username": username.lower()}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return user


"""
    Modificar usuario:
        - Obtener la conexion DB
        - Validar si hay datos nuevo
        - Actualizar usuario en MongoDB Atlas
"""
async def update_user(username: str, user: UserUpdate):
    collection = await get_db_user()  # Obtener conexión en cada petición
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    result = await collection.update_one({"username": username.lower()}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario actualizado satisfactoriamente"}


"""
    Eliminar usuario:
        - Obtener la conexion DB
        - Eliminar usuario en MongoDB Atlas
"""
async def delete_user(username: str):
    collection = await get_db_user()  # Obtener conexión en cada petición
    result = await collection.delete_one({"username": username.lower()})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "usuario borrado satisfactoriamente"}
