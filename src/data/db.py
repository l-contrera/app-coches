import os
from sqlmodel import create_engine, SQLModel, Session, select
from src.models.coche import Coche

DATABASE_URL = os.environ["DATABASE_URL"]

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
