# Gestor de Tareas — Proyecto de formación

Backend de gestión de tareas construido con FastAPI y SQLite. Usado como proyecto de ejemplo en el módulo de formación en IA aplicada al desarrollo.

## Requisitos previos

- Python 3.10 o superior
- Terminal (macOS/Linux) o PowerShell (Windows)

Comprueba tu versión de Python:

```bash
python3 --version
```

---

## Instalación

### 1. Clona o descarga el proyecto

```bash
git clone <url-del-repositorio>
cd AyuntamientoMurcia
```

### 2. Crea el entorno virtual

```bash
python3 -m venv .venv
```

### 3. Activa el entorno virtual

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

El prompt del terminal cambiará a `(.venv)` cuando el entorno esté activo.

### 4. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 5. Carga los datos de prueba

```bash
python3 seed.py
```

Esto crea el fichero `tareas.db` con 3 usuarios y 5 tareas de ejemplo.

### 6. Arranca el servidor

```bash
uvicorn app.main:app --reload
```

El servidor queda escuchando en `http://127.0.0.1:8000`.  
El flag `--reload` reinicia el servidor automáticamente al guardar cambios en el código.

---

## Verificación

Abre en el navegador:

- **Documentación interactiva (Swagger):** http://127.0.0.1:8000/docs
- **Documentación alternativa (ReDoc):** http://127.0.0.1:8000/redoc
- **Endpoint raíz:** http://127.0.0.1:8000/

O comprueba desde terminal:

```bash
curl http://127.0.0.1:8000/tareas/
```

---

## Endpoints disponibles

| Método   | Ruta                      | Descripción                              |
|----------|---------------------------|------------------------------------------|
| `GET`    | `/tareas/`                | Listar tareas (filtrables por estado, prioridad, usuario) |
| `POST`   | `/tareas/`                | Crear tarea                              |
| `GET`    | `/tareas/{id}`            | Obtener tarea por ID                     |
| `PUT`    | `/tareas/{id}`            | Actualizar tarea                         |
| `PATCH`  | `/tareas/{id}/estado`     | Cambiar estado (respeta la máquina de estados) |
| `DELETE` | `/tareas/{id}`            | Eliminar tarea                           |
| `GET`    | `/usuarios/`              | Listar usuarios                          |
| `POST`   | `/usuarios/`              | Crear usuario                            |
| `GET`    | `/usuarios/{id}`          | Obtener usuario por ID                   |
| `DELETE` | `/usuarios/{id}`          | Eliminar usuario                         |

### Estados y transiciones permitidas

```
PENDIENTE ──► EN_PROGRESO ──► COMPLETADA
    │               │
    ▼               ▼
CANCELADA       CANCELADA ──► PENDIENTE
```

---

## Reiniciar la base de datos

Para volver al estado inicial borra el fichero de base de datos y ejecuta el seed de nuevo:

```bash
rm tareas.db
python3 seed.py
```

---

## Estructura del proyecto

```
AyuntamientoMurcia/
├── app/
│   ├── database.py        # Conexión SQLite y sesión
│   ├── models.py          # Modelos SQLAlchemy y enums
│   ├── schemas.py         # Schemas Pydantic (request/response)
│   ├── main.py            # Aplicación FastAPI
│   └── routers/
│       ├── tareas.py      # Rutas de tareas
│       └── usuarios.py    # Rutas de usuarios
├── seed.py                # Script de datos de prueba
├── laboratorio_prompts.md # Prompts para el laboratorio de formación
├── requirements.txt
└── README.md
```
