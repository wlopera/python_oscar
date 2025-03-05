from fastapi import FastAPI
from crud.user_routes import router as user_router  # Importar las rutas de usuario

app = FastAPI()


@app.get("/")
def read_root():
    print("Imprimir Hola Mundo en la consola..")
    return {"message": "Hola Mundo"}


# Incluir el router de usuarios
app.include_router(user_router)
