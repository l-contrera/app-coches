from datetime import date
from sqlmodel import SQLModel, Field

class Coche(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: str
    modelo: str
    año: int
    disponible: bool
    fecha_ingreso: date
