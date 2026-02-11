from sqlmodel import create_engine, SQLModel, Session
from models.coche import Coche
import os

DATABASE_URL = os.environ["postgresql://coches_pri9_user:viGYhIm3EVu3hNSAvxEURVR46yYf0dCj@dpg-d65qj0ali9vc738pfcrg-a.oregon-postgres.render.com/coches_pri9"]

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.exec(select(Coche)).first() is None:
            session.add(Coche(marca="Toyota", modelo="Corolla", año=2020, disponible=True, fecha_ingreso="2023-05-10"))
            session.add(Coche(marca="Ford", modelo="Mustang", año=2018, disponible=False, fecha_ingreso="2022-11-01"))
            session.add(Coche(marca="BMW", modelo="Serie 3", año=2021, disponible=True, fecha_ingreso="2023-09-20"))
            session.commit()
