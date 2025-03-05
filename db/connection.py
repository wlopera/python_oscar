import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno

# Configuración de MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
print(f"Mongo URI: {MONGO_URI}")  # Esto es solo para debug, recuerda eliminarlo después
db = client[DB_NAME]


# Función para cerrar la conexión
def close_db_connection():
    client.close()
