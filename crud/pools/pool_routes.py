from fastapi import APIRouter
from models.pools_models import Category
from crud.pools.pool_crud import create_pool, get_pool, add_category, update_category, delete_category

from models.pools_models import  Pool
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