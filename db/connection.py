import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno

# Configuración de MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


"""
    Consulta de la collection users de MongoDB Atlas
"""
async def get_db_user():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    return db["users"]


"""
    Consulta de la collection pools de MongoDB Atlas
"""
async def get_db_pool():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    return db["pools"]

