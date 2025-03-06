from pydantic import BaseModel
from typing import List


# Modelo para cada categoría
class Category(BaseModel):
    name: str
    nominees: List[str]


class Option(BaseModel):
    category: str  # Nombre de la categoría
    nominee: str   # Nominado seleccionado
    score: int     # Puntuación del nominador


# Modelo de Resultado
class ResultOption(BaseModel):
    user: str           # Nombre del participante (ej. "william")
    options: List[Option]  # Lista de opciones que contienen categorías, nominados y puntajes


# Modelo de la quiniela
class Pool(BaseModel):
    name: str
    categories: List[Category]
    results: List[ResultOption]  # Lista de resultados de los participantes

