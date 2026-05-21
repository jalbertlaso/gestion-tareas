from fastapi import FastAPI

from .database import Base, engine
from .routers import tareas, usuarios

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Tareas — Ayuntamiento",
    description="API de ejemplo para formación en IA aplicada al desarrollo.",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(tareas.router)


@app.get("/", tags=["raíz"])
def raiz():
    return {"mensaje": "API de gestión de tareas operativa", "docs": "/docs"}
