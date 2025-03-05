from fastapi import FastAPI
from db.connection import db, close_db_connection  # Importar la conexión a la base de datos
from crud.user_routes import router as user_router  # Importar las rutas de usuario
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()  # Cargar variables de entorno


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db["users"].create_index("username", unique=True)
    yield  # Dejar que la app corra
    close_db_connection()  # Cerrar conexión en shutdown

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)


@app.get("/")
def read_root():
    print("Imprimir Hola Mundo en la consola..")
    return {"message": "Hola Mundo"}


@app.get("/test")
def test():
    return {"message": "Test ruta funciona!"}


# Incluir el router de usuarios
app.include_router(user_router)
