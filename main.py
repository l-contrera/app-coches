from fastapi import FastAPI, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from sqlmodel import Session, select
from typing import Annotated
from src.models.coche import Coche
from src.data.db import init_db, get_session
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    mensaje = "Bienvenido al concesionario"
    return templates.TemplateResponse("index.html", {"request": request, "mensaje": mensaje})

@app.get("/coches/web", response_class=HTMLResponse)
async def ver_coches(request: Request, session: SessionDep):
    coches = session.exec(select(Coche)).all()
    return templates.TemplateResponse("coches.html", {"request": request, "coches": coches})

@app.get("/coches/web/{coche_id}", response_class=HTMLResponse)
async def detalle_coche(coche_id: int, request: Request, session: SessionDep):
    coche = session.get(Coche, coche_id)
    if coche is None:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return templates.TemplateResponse("coches_detalle.html", {"request": request, "coche": coche})

@app.get("/coches", response_model=list[Coche])
async def lista_coches(session: SessionDep):
    return session.exec(select(Coche)).all()

@app.post("/coches", response_model=Coche, status_code=201)
async def crear_coche(coche: Coche, session: SessionDep):
    session.add(coche)
    session.commit()
    session.refresh(coche)
    return coche

@app.put("/coches/{coche_id}", response_model=Coche)
async def actualizar_coche(coche_id: int, coche_actualizado: Coche, session: SessionDep):
    coche = session.get(Coche, coche_id)
    if coche is None:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    coche.marca = coche_actualizado.marca
    coche.modelo = coche_actualizado.modelo
    coche.año = coche_actualizado.año
    coche.disponible = coche_actualizado.disponible
    coche.fecha_ingreso = coche_actualizado.fecha_ingreso
    session.add(coche)
    session.commit()
    session.refresh(coche)
    return coche

@app.delete("/coches/{coche_id}", status_code=204)
async def eliminar_coche(coche_id: int, session: SessionDep):
    coche = session.get(Coche, coche_id)
    if coche is None:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    session.delete(coche)
    session.commit()
    return None
