"""Carga datos de prueba en la base de datos (idempotente: borra y recrea los datos)."""
from app.database import SessionLocal, Base, engine
from app.models import Usuario, Tarea, EstadoTarea, PrioridadTarea

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

usuarios = [
    Usuario(nombre="Ana García", email="ana.garcia@murcia.es"),
    Usuario(nombre="Carlos Martínez", email="carlos.martinez@murcia.es"),
    Usuario(nombre="Laura Pérez", email="laura.perez@murcia.es"),
]
db.add_all(usuarios)
db.commit()
for u in usuarios:
    db.refresh(u)

tareas = [
    Tarea(titulo="Migrar base de datos de padrón", descripcion="Actualizar esquema a la versión 3.2", prioridad=PrioridadTarea.URGENTE, usuario_id=usuarios[0].id),
    Tarea(titulo="Revisar accesibilidad web", descripcion="Cumplimiento WCAG 2.1 AA en portal ciudadano", prioridad=PrioridadTarea.ALTA, usuario_id=usuarios[1].id),
    Tarea(titulo="Documentar API de tributos", prioridad=PrioridadTarea.MEDIA),
    Tarea(titulo="Actualizar certificados SSL", prioridad=PrioridadTarea.ALTA, usuario_id=usuarios[2].id),
    Tarea(titulo="Reunión de seguimiento Q2", prioridad=PrioridadTarea.BAJA),
]
db.add_all(tareas)
db.commit()

# Avanzar el estado de algunas tareas
tareas[0].estado = EstadoTarea.EN_PROGRESO
tareas[1].estado = EstadoTarea.COMPLETADA
db.commit()

db.close()
print("Datos de prueba cargados correctamente.")
