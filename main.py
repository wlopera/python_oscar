from fastapi import FastAPI
from crud.users.user_routes import router as user_router  # Importar las rutas de los usuario
from crud.pools.pool_routes import router as pool_router  # Importar las rutas de las quinielas

app = FastAPI()

# Incluir el router de los usuarios
app.include_router(user_router)

# Incluir el router de las quinielas
app.include_router(pool_router)
