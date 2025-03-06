from fastapi import APIRouter
from models.pools_models import Category, Pool, ResultOption
from crud.pools.pool_crud import (create_pool, get_pool, add_category,
                                  update_category,delete_category, add_result, update_result,
                                  delete_result, delete_user_results, get_results)

router = APIRouter()

@router.post("/pools/")
async def create_pool_endpoint(pool: Pool):
    return await create_pool(pool)

@router.get("/pools/{pool_name}")
async def read_pool_endpoint(pool_name: str):
    return await get_pool(pool_name)

@router.post("/pools/{pool_name}/categories/")
async def add_category_endpoint(pool_name: str, category: Category):
    return await add_category(pool_name, category)

@router.put("/pools/{pool_name}/categories/{category_name}")
async def update_category_endpoint(pool_name: str, category_name: str, updated_category: Category):
    return await update_category(pool_name, category_name, updated_category)

@router.delete("/pools/{pool_name}/categories/{category_name}")
async def delete_category_endpoint(pool_name: str, category_name: str):
    return await delete_category(pool_name, category_name)

# Nuevo endpoint para agregar un resultado
@router.post("/pools/{pool_name}/results/")
async def add_result_endpoint(pool_name: str, resultOption: ResultOption):
    return await add_result(pool_name, resultOption)


@router.put("/pools/{pool_name}/results/{result_name}")
async def update_result_endpoint(pool_name: str, result_name: str, updated_result: ResultOption):
    return await update_result(pool_name, result_name, updated_result)


@router.delete("/pools/{pool_name}/results/{result_user}/{category}")
async def delete_result_endpoint(pool_name: str, result_user: str, category: str):
    # Llamar a la función que elimina el resultado
    return await delete_result(pool_name, result_user, category)


@router.delete("/pools/{pool_name}/results/{result_user}")
async def delete_user_results_endpoint(pool_name: str, result_user: str):
    return await delete_user_results(pool_name, result_user)


@router.get("/pools/{pool_name}/results/")
async def get_results_endpoint(pool_name: str):
    return await get_results(pool_name)

