from fastapi import FastAPI
from db.connection import db, close_db_connection  # Importar la conexión a la base de datos
from crud.user_routes import router as user_router  # Importar las rutas de usuario
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()  # Cargar variables de entorno


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db["users"].create_index("username", unique=True)
    yield  # Dejar que la app corra
    close_db_connection()  # Cerrar conexión en shutdown

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    print("Imprimir Hola Mundo en la consola..")
    return {"message": "Hola Mundo"}


# Incluir el router de usuarios
app.include_router(user_router)
