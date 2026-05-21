from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import EstadoTarea, PrioridadTarea, Tarea, TRANSICIONES_VALIDAS, Usuario
from ..schemas import CambioEstado, TareaActualizar, TareaCrear, TareaLeer

router = APIRouter(prefix="/tareas", tags=["tareas"])


@router.get("/", response_model=list[TareaLeer])
def listar_tareas(
    estado: Optional[EstadoTarea] = Query(None),
    prioridad: Optional[PrioridadTarea] = Query(None),
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    consulta = db.query(Tarea)
    if estado:
        consulta = consulta.filter(Tarea.estado == estado)
    if prioridad:
        consulta = consulta.filter(Tarea.prioridad == prioridad)
    if usuario_id:
        consulta = consulta.filter(Tarea.usuario_id == usuario_id)
    return consulta.all()


@router.post("/", response_model=TareaLeer, status_code=status.HTTP_201_CREATED)
def crear_tarea(datos: TareaCrear, db: Session = Depends(get_db)):
    if datos.usuario_id:
        _verificar_usuario(datos.usuario_id, db)

    tarea = Tarea(**datos.model_dump())
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


@router.get("/{tarea_id}", response_model=TareaLeer)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)):
    return _obtener_o_404(tarea_id, db)


@router.put("/{tarea_id}", response_model=TareaLeer)
def actualizar_tarea(tarea_id: int, datos: TareaActualizar, db: Session = Depends(get_db)):
    tarea = _obtener_o_404(tarea_id, db)

    if datos.usuario_id is not None:
        _verificar_usuario(datos.usuario_id, db)

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(tarea, campo, valor)

    db.commit()
    db.refresh(tarea)
    return tarea


@router.patch("/{tarea_id}/estado", response_model=TareaLeer)
def cambiar_estado(tarea_id: int, cambio: CambioEstado, db: Session = Depends(get_db)):
    tarea = _obtener_o_404(tarea_id, db)

    destinos_validos = TRANSICIONES_VALIDAS[tarea.estado]
    if cambio.estado not in destinos_validos:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Transición no permitida: {tarea.estado} → {cambio.estado}. "
                f"Destinos válidos: {[e.value for e in destinos_validos] or 'ninguno'}"
            ),
        )

    tarea.estado = cambio.estado
    db.commit()
    db.refresh(tarea)
    return tarea


@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = _obtener_o_404(tarea_id, db)
    db.delete(tarea)
    db.commit()


# ── helpers ───────────────────────────────────────────────────────────────────

def _obtener_o_404(tarea_id: int, db: Session) -> Tarea:
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


def _verificar_usuario(usuario_id: int, db: Session) -> None:
    if not db.query(Usuario).filter(Usuario.id == usuario_id).first():
        raise HTTPException(status_code=404, detail=f"Usuario {usuario_id} no encontrado")
