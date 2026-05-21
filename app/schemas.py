from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

from .models import EstadoTarea, PrioridadTarea


# ── Usuario ───────────────────────────────────────────────────────────────────

class UsuarioCrear(BaseModel):
    nombre: str
    email: str

    @field_validator("email")
    @classmethod
    def email_minusculas(cls, v: str) -> str:
        return v.lower().strip()


class UsuarioLeer(BaseModel):
    id: int
    nombre: str
    email: str
    creado_en: datetime

    model_config = {"from_attributes": True}


# ── Tarea ─────────────────────────────────────────────────────────────────────

class TareaCrear(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    prioridad: PrioridadTarea = PrioridadTarea.MEDIA
    usuario_id: Optional[int] = None


class TareaActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    prioridad: Optional[PrioridadTarea] = None
    usuario_id: Optional[int] = None


class CambioEstado(BaseModel):
    estado: EstadoTarea


class TareaLeer(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    estado: EstadoTarea
    prioridad: PrioridadTarea
    usuario_id: Optional[int]
    creada_en: datetime
    actualizada_en: datetime
    asignado_a: Optional[UsuarioLeer] = None

    model_config = {"from_attributes": True}
