# Laboratorio: El mismo problema, tres prompts distintos

## Problema a resolver
Añadir un endpoint `GET /tareas/resumen` que devuelva estadísticas agregadas:
total de tareas, cuántas hay en cada estado y cuántas están sin asignar.

---

## Prompt 1 — Zero-shot (básico)

```
Añade un endpoint GET /tareas/resumen que devuelva estadísticas de las tareas.
```

**Qué observar:** ¿El modelo infiere la estructura del proyecto? ¿Hay que
corregir imports o nombres de modelos? ¿Funciona a la primera?

---

## Prompt 2 — Few-shot con contexto de arquitectura

```
Actúa como desarrollador Python senior experto en FastAPI y SQLAlchemy.

El proyecto tiene esta estructura:
- app/models.py     → modelos SQLAlchemy: Tarea, Usuario, EstadoTarea (enum)
- app/schemas.py    → esquemas Pydantic (patrón TareaLeer, UsuarioLeer)
- app/routers/tareas.py → router montado en /tareas

Ejemplo de endpoint existente en tareas.py:
    @router.get("/", response_model=list[TareaLeer])
    def listar_tareas(estado: Optional[EstadoTarea] = Query(None), db: Session = Depends(get_db)):
        consulta = db.query(Tarea)
        if estado:
            consulta = consulta.filter(Tarea.estado == estado)
        return consulta.all()

Añade un endpoint GET /tareas/resumen que devuelva:
    { "total": 10, "por_estado": {"pendiente": 4, ...}, "sin_asignar": 3 }
Usa func.count de SQLAlchemy para las agregaciones. No uses Python para contar.
```

**Qué observar:** ¿Se ajusta a los nombres reales del código? ¿Usa SQLAlchemy
correctamente sin iterar en Python? ¿Genera un schema Pydantic para la respuesta?

---

## Prompt 3 — Chain-of-thought + rol + contexto completo

```
Actúa como desarrollador Python senior experto en FastAPI y SQLAlchemy.

Contexto del proyecto:
- app/models.py: modelos SQLAlchemy Tarea (campos: id, titulo, estado, prioridad,
  usuario_id) y Usuario. EstadoTarea es un enum con valores:
  pendiente, en_progreso, completada, cancelada.
- app/schemas.py: esquemas Pydantic. Convención de nombres: clases terminan en Leer/Crear.
- app/routers/tareas.py: router con prefix="/tareas". Usa Depends(get_db) para la sesión.

Tarea: añadir GET /tareas/resumen con respuesta:
    { "total": int, "por_estado": dict[str, int], "sin_asignar": int }

Antes de escribir código, razona paso a paso:
1. ¿Qué consulta SQL necesito para cada campo del resumen?
2. ¿Cómo traducir cada consulta a SQLAlchemy (func.count, group_by, filter)?
3. ¿Necesito un schema Pydantic nuevo o puedo usar dict?
4. ¿Dónde coloco la ruta para que FastAPI no la confunda con /{tarea_id}?

Después escribe el código listo para copiar en los archivos indicados.
```

**Qué observar:** ¿El razonamiento previo evita errores de routing (/resumen vs /{id})?
¿La consulta es más eficiente? ¿El código necesita menos revisión?

---

## Guía de reflexión post-laboratorio

| Criterio            | Zero-shot | Few-shot | Chain-of-thought |
|---------------------|-----------|----------|------------------|
| Correcto a la primera |         |          |                  |
| Imports correctos   |           |          |                  |
| Usa SQL en vez de Python |      |          |                  |
| Orden de rutas correcto |       |          |                  |
| Tiempo hasta funcionar |        |          |                  |

**Pregunta clave:** ¿En qué tipo de tarea diaria de vuestro equipo aplicaríais
cada técnica?
