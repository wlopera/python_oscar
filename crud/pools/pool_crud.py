from fastapi import HTTPException
from models.pools_models import Pool, Category
from db.connection import get_db_pool
from utilities.util import str_object_id
"""
    Crear quiniela:
        - Obtener la conexion DB
        - Validar si la quiniela no existe (nuevo)
        - Insertar quiniela en MongoDB Atlas
"""
async def create_pool(pool: Pool):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    if await collection.find_one({"name": pool.name}):
        raise HTTPException(status_code=400, detail="La quiniela ya existe")
    await collection.insert_one(pool.dict())
    return {"message": "Quiniela creada exitosamente"}


"""
    Concultar quiniela por nombre:
        - Obtener la conexion DB
        - Retornar datos de la quiniela en MongoDB Atlas
"""
async def get_pool(pool_name: str):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    pool = await collection.find_one({"name": pool_name})
    if not pool:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    # Convertir el campo '_id' de ObjectId a str
    pool = str_object_id(pool)

    return pool


"""
    Agregar una categoría a una quiniela existente:
        - Obtener la conexion DB
        - Validar si hay datos nuevo
        - Agregar categoria en MongoDB Atlas
"""


async def add_category(pool_name: str, category: Category):
    collection = await get_db_pool()  # Obtener conexión a la base de datos

    # Verificar si la categoría ya está presente en la quiniela
    existing_pool = await collection.find_one({"name": pool_name})
    if existing_pool and any(c['name'] == category.name for c in existing_pool.get("categories", [])):
        raise HTTPException(status_code=400, detail="La categoría ya existe en esta quiniela")

    # Agregar la nueva categoría
    result = await collection.update_one(
        {"name": pool_name},
        {"$push": {"categories": category.dict()}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    return {"message": "Categoría agregada exitosamente"}


"""
    Actualizar una categoría dentro de una quiniela:
        - Obtener la conexion DB
        - Validar si hay datos nuevo
        - Actualizar categoria en MongoDB Atlas
"""
async def update_category(pool_name: str, category_name: str, updated_category: Category):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    pool_data = {k: v for k, v in updated_category.dict().items() if v is not None}
    if not pool_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    result = await collection.update_one(
        {"name": pool_name, "categories.name": category_name},
        {"$set": {"categories.$": updated_category.dict()}}
    )
    # Verifica si se realizó alguna modificación en la colección
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela o categoría no encontrada")
    if result.modified_count == 0:
        return {"message": "No se realizaron cambios en la categoría"}

    return {"message": "Categoría actualizada exitosamente"}

"""
    Eliminar una categoría de una quiniela:
        - Obtener la conexion DB
        - Eliminar categoria en MongoDB Atlas
"""
async def delete_category(pool_name: str, category_name: str):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    result = await collection.update_one(
        {"name": pool_name},
        {"$pull": {"categories": {"name": category_name}}}
    )

    # Verifica si la quiniela o categoría no se encontró
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    # Verifica si la categoría fue efectivamente eliminada
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o no eliminada")

    return {"message": "Categoría eliminada exitosamente"}
