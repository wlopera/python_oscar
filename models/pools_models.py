from pydantic import BaseModel
from typing import List


# Modelo para cada categoría
class Category(BaseModel):
    name: str
    nominees: List[str]


# Modelo de la quiniela
class Pool(BaseModel):
    name: str
    categories: List[Category]