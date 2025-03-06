from fastapi import HTTPException
from models.pools_models import Pool, Category, ResultOption
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


"""
    Agregar resultado de una quiniela:
        - Obtener la conexion DB
        - Agregar resultado en MongoDB Atlas
"""


async def add_result(pool_name: str, resultOption: ResultOption):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    # Verificar si la quiniela existe
    existing_pool = await collection.find_one({"name": pool_name})
    if not existing_pool:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    # Buscar si el usuario ya tiene un resultado
    existing_result = await collection.find_one(
        {"name": pool_name, "results.user": resultOption.user}
    )

    if existing_result:
        # Si el usuario ya tiene un resultado, agregamos la nueva opción a su lista de opciones
        result_dict = resultOption.dict()
        await collection.update_one(
            {"name": pool_name, "results.user": resultOption.user},
            {"$push": {"results.$.options": {"category": result_dict["options"][0]["category"],
                                             "nominee": result_dict["options"][0]["nominee"],
                                             "score": result_dict["options"][0]["score"]}}}
        )
    else:
        # Si el usuario no tiene un resultado, agregamos un nuevo documento a `results`
        result_dict = resultOption.dict()
        result_dict["user"] = resultOption.user  # Asegurarse de que el nombre sea único
        await collection.update_one(
            {"name": pool_name},
            {"$push": {"results": result_dict}}  # Añadir el nuevo resultado a la lista de resultados
        )

    return {"message": "Resultado agregado exitosamente"}


"""
    Consultar resultados de una quiniela:
        - Obtener la conexion DB
        - Consultar resultados en MongoDB Atlas
"""
async def get_results(pool_name: str):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    pool = await collection.find_one({"name": pool_name})
    if not pool:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    return pool.get("results", [])


"""
    Modificar resultado de una quiniela:
        - Obtener la conexion DB
        - Modificar resultado en MongoDB Atlas
"""
async def update_result(pool_name: str, result_user: str, updated_result: ResultOption):
    collection = await get_db_pool()  # Obtener conexión en cada petición

    # Filtrar los campos que no sean None
    result_data = {k: v for k, v in updated_result.dict().items() if v is not None}
    if not result_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    # Actualizar las opciones dentro del array `results` para el usuario específico
    result = await collection.update_one(
        {"name": pool_name, "results.user": result_user},
        {"$set": {
            "results.$.options": updated_result.options  # Actualizar solo las opciones
        }}
    )

    # Verifica si se realizó alguna modificación en la colección
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela o resultado no encontrado")

    if result.modified_count == 0:
        return {"message": "No se realizaron cambios en el resultado"}

    return {"message": "Resultado actualizado exitosamente"}



"""
    Eliminar resultado de una quiniela:
        - Obtener la conexion DB
        - Eliminar resultado en MongoDB Atlas
"""
async def delete_result(pool_name: str, result_user: str, category: str):
    collection = await get_db_pool()  # Obtener conexión en cada petición

    # Realizamos la operación para eliminar todas las opciones de la categoría especificada para el usuario
    result = await collection.update_one(
        {"name": pool_name, "results.user": result_user},  # Buscar la quiniela y el usuario
        {"$pull": {"results.$.options": {"category": category}}}  # Eliminar todas las opciones de esa categoría
    )

    # Verifica si la quiniela o el usuario no se encontraron
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela o usuario no encontrado")

    # Verifica si el resultado fue efectivamente eliminado
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Resultado no encontrado o no eliminado")

    return {"message": f"Resultados de la categoría '{category}' eliminados exitosamente para el usuario '{result_user}'"}


"""
    Eliminar un usuario de los resultados de una quiniela:
        - Obtener la conexion DB
        - Eliminar usuario de los resultados en MongoDB Atlas
"""
async def delete_user_results(pool_name: str, result_user: str):
    collection = await get_db_pool()  # Obtener conexión en cada petición
    result = await collection.update_one(
        {"name": pool_name},
        {"$pull": {"results": {"user": result_user}}}  # Elimina todos los resultados del usuario
    )

    # Verifica si la quiniela no se encontró
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Quiniela no encontrada")

    # Verifica si el usuario no tiene resultados o no se eliminaron
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Resultados no encontrados para el usuario")

    return {"message": f"Todos los resultados de {result_user} eliminados exitosamente"}
