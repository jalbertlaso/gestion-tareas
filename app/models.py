from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
import enum

from .database import Base


class EstadoTarea(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class PrioridadTarea(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


# Transiciones de estado permitidas
TRANSICIONES_VALIDAS: dict[EstadoTarea, set[EstadoTarea]] = {
    EstadoTarea.PENDIENTE: {EstadoTarea.EN_PROGRESO, EstadoTarea.CANCELADA},
    EstadoTarea.EN_PROGRESO: {EstadoTarea.COMPLETADA, EstadoTarea.CANCELADA, EstadoTarea.PENDIENTE},
    EstadoTarea.COMPLETADA: set(),
    EstadoTarea.CANCELADA: {EstadoTarea.PENDIENTE},
}


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tareas = relationship("Tarea", back_populates="asignado_a")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Enum(EstadoTarea), default=EstadoTarea.PENDIENTE, nullable=False)
    prioridad = Column(Enum(PrioridadTarea), default=PrioridadTarea.MEDIA, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    creada_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    actualizada_en = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    asignado_a = relationship("Usuario", back_populates="tareas")
