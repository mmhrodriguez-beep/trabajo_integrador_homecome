# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
Primero está el alcance completo del proyecto; al final, la devolución de cada semana.

**Grupo:** Matías Rodríguez Hrdy, Christian López
**Tema:** HomeCome — Casa inteligente

---

# Alcances de este proyecto

Esto es lo que hay que entregar. Lo que no está acá, no se pide.

## Reglas comunes a todos los grupos

### Stack
- Python + **FastAPI** + Uvicorn.
- Datos en **SQLite** (con `sqlite3`, como en la Clase 16; SQLAlchemy es opcional).
- Repositorio en GitHub con commits de **todos** los integrantes.
- API desplegada **en producción con Gunicorn** en Render, con URL pública y `/docs` funcionando (ver abajo).

### Despliegue a producción (Render + Gunicorn)

En tu compu desarrollás con `uvicorn main:app --reload`. En producción corre **Gunicorn** como administrador de procesos, con workers de Uvicorn adentro.

> Gunicorn **no funciona en Windows**. Localmente seguí usando `uvicorn`; Gunicorn corre en el servidor (Linux).

`requirements.txt` debe incluir:
```
fastapi
uvicorn
uvicorn-worker
gunicorn
```

En Render → **New → Web Service** → conectás el repo, y configurás:

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python seed.py && gunicorn main:app -k uvicorn_worker.UvicornWorker -w 2 -b 0.0.0.0:$PORT` |

La clave viaja en el código, así que no hay que configurar nada más en Render.

- El seed corre **una sola vez antes** de levantar Gunicorn. Si lo pusieras adentro de `main.py`, cada worker lo ejecutaría por su cuenta y podrían cargar los datos duplicados.
- El plan gratis se duerme tras ~15 min sin uso (la primera visita tarda ~1 min) y su disco se borra al reiniciar: por eso el seed.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- Unos **10 registros de ejemplo** por tabla. Siempre **datos ficticios**.
- Un script de carga inicial `seed.py` que crea las tablas y carga los datos **si la base está vacía**. Se ejecuta antes de levantar el servidor. En Render el disco se borra al reiniciar: así la API siempre arranca con datos.
- El archivo `.db` **no se sube** a GitHub (agregalo al `.gitignore`); se genera solo.

### Seguridad: TODOS los endpoints van protegidos
- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- La clave se define como una constante al principio de `main.py`. Más adelante en la carrera van a ver cómo sacarla del código con variables de entorno; por ahora, así.
- Como la clave está a la vista en el repo, **los datos son todos ficticios** y no se usa esta API para nada real.
- Sin clave o con clave incorrecta → **401**.

Se protege toda la app de una vez:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

CLAVE = "clave-de-prueba-2026"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.

---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param, `SELECT ... WHERE` |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o SQL) |
| 6 | Alta | `POST /cosas` | Insertar en la base, con modelo **Pydantic** |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Deploy:** URL pública en Render con `/docs` operativo.
- **README:** qué hace la API, lista de endpoints, cómo usar la API key, cómo correrla localmente, y declaración de uso de IA si la usaron.

## Nivel B — opcional

Existe un Nivel B que suma hasta 1 punto sobre la nota final. **No se preocupen por eso todavía:** lo vemos en clase más adelante, cuando el Nivel A esté andando.

---

## Alcance de este grupo

### Grupo 4 · HomeCome — Casa inteligente
**Integrantes:** Matías Rodríguez Hrdy, Christian López

**Tablas**
- `habitaciones`: id, nombre, piso
- `dispositivos`: id, nombre, tipo (luz / sensor / cerradura / termostato), estado, habitacion_id (FK)
- `eventos`: id, fecha, descripcion, dispositivo_id (FK)

**Endpoints Nivel A**
1. `GET /dispositivos?tipo=luz&estado=encendido`
2. `GET /dispositivos/{id}`
3. `GET /habitaciones/{id}/dispositivos`
4. `GET /eventos?dispositivo_id=3`
5. `GET /resumen` → cantidad de dispositivos encendidos por habitación
6. `POST /dispositivos`


---

## Fuera de alcance (para todos)

No se pide y **no suma**:
- Frontend o páginas web.
- Login de usuarios, registro, JWT.
- Bases de datos externas (PostgreSQL, MySQL, etc.).
- Docker.
- Integración con IA o con el chatbot (eso corresponde a Análisis de Sistemas).
- Pagos, facturación, envío de mails, hardware real.

## Entregables

1. Repositorio GitHub: `main.py`, script de seed, `requirements.txt`, `README.md`, commits de todos.
2. URL pública en Render con `/docs` funcionando.
3. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
4. Defensa oral: demo en vivo desde `/docs` y preguntas sobre el código.

---

# Devolución semanal

## 23/09

**Lo que hay:** README y `.gitignore`, sin código desde el 16/09.

**Sobre el tema:** aprobado. Como los datos de una casa son sensibles, todos los endpoints van con clave, igual que el resto de los grupos.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` con las 3 tablas: `habitaciones`, `dispositivos` (con `habitacion_id`) y `eventos` (con `dispositivo_id`).
3. Tipos de dispositivo sugeridos: luz, sensor, cerradura, termostato.

**Fuera de alcance:** dispositivos reales, hardware, MQTT y tiempo real. La API sirve datos, nada más.
