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
- Datos en **SQLite** usando **SQLAlchemy** (ORM): las tablas se definen como clases de Python y las consultas se hacen con métodos, sin escribir SQL a mano. **No se usa Pydantic**: las validaciones se hacen a mano en Python. Guía con ejemplo completo: [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md).
- Repositorio en GitHub con commits de **todos** los integrantes.
- API desplegada **en producción con Gunicorn** en Render, con URL pública y `/docs` funcionando (ver abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 08/10:** ahora va **todo en inglés**, también tablas, columnas y rutas. Reemplaza el criterio del 24/09.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params también en inglés**. Ejemplo: `class Student(Base)` con `__tablename__ = "students"`, columna `career_id` y ruta `GET /students`.
- El alcance de cada grupo lista las tablas y los endpoints en español **solo como referencia**: tradúzcanlos al inglés y usen **el mismo nombre en todos los archivos** (`db.py`, `seed.py`, `main.py`, `validation.py`).
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Despliegue a producción (Render + Gunicorn)

En tu compu desarrollás con `uvicorn main:app --reload`. En producción corre **Gunicorn** como administrador de procesos, con workers de Uvicorn adentro.

> Gunicorn **no funciona en Windows**. Localmente seguí usando `uvicorn`; Gunicorn corre en el servidor (Linux).

`requirements.txt` debe incluir:
```
fastapi
uvicorn
uvicorn-worker
gunicorn
sqlalchemy
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
- Un script de carga inicial `seed.py` que crea las tablas (`create_all`) y carga los datos **si la base está vacía** (ver sección 9 de la guía). Se ejecuta antes de levantar el servidor. En Render el disco se borra al reiniciar: así la API siempre arranca con datos.
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
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param, `select(...).where(...)` |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea (`relationship` o filtro por FK) |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o con `func` de SQLAlchemy) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo como `dict`, **validar a mano** (400 si está mal) e insertar con la sesión |

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

**📌 Novedad:** la base se maneja con **SQLAlchemy** (ORM) y **sin Pydantic**; las validaciones del `POST` van a mano. Hay una guía con ejemplo completo en [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md) y el código en `guias/pokedex/`. Agreguen `sqlalchemy` a `requirements.txt`.

**Lo que hay:** README y `.gitignore`, sin código desde el 16/09.

**Sobre el tema:** aprobado. Como los datos de una casa son sensibles, todos los endpoints van con clave, igual que el resto de los grupos.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` con las 3 tablas: `habitaciones`, `dispositivos` (con `habitacion_id`) y `eventos` (con `dispositivo_id`).
3. Tipos de dispositivo sugeridos: luz, sensor, cerradura, termostato.

**Fuera de alcance:** dispositivos reales, hardware, MQTT y tiempo real. La API sirve datos, nada más.

## 24/09

**📌 Criterio de nombres.** Variables, funciones y clases en **inglés**; tablas, columnas y rutas como en el alcance; comentarios en inglés para la entrega final. Está detallado arriba en *Reglas comunes* y la guía ya lo aplica.

**Lo que hay:** sin cambios desde el 16/09. Solo README y `.gitignore`. Ningún commit de Christian todavía.

Todos los demás grupos ya tienen código o base de datos. Están quedando atrás y el calendario no espera: el 30/09 la meta son los endpoints 1 a 3.

**Próximos pasos (urgente)**
1. `main.py` con `app = FastAPI()` y un endpoint que devuelva JSON. Probarlo con `uvicorn main:app --reload` y `/docs`.
2. `seed.py` con **SQLAlchemy** (ver [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)): `habitaciones`, `dispositivos` (con `habitacion_id`) y `eventos` (con `dispositivo_id`), ~10 registros por tabla.
3. `requirements.txt` con `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.
4. Repártanse: uno el seed y otro `main.py`, así los dos aparecen en los commits.

## 08/10

**📌 Cambio de criterio: todo en inglés.** Ahora también las **tablas, columnas, rutas y query params** van en inglés, igual que el README, los docstrings y los mensajes de la API. Reemplaza lo dicho el 24/09; está detallado arriba en *Nombres en el código*. El alcance sigue listando los nombres en español solo como referencia.

**📌 Guía nueva (opcional):** [guias/variables_de_entorno.md](guias/variables_de_entorno.md), para sacar la clave del código con un `.env`.

**Lo que hay:** sin cambios. El repo sigue igual que el **16/09**: solo el README de una línea y el `.gitignore`. Van más de tres semanas sin un commit, y Christian todavía no tiene ninguno.

**⚠️ Están muy atrasados.** Hay grupos con los seis endpoints funcionando y el resto ya tiene al menos la base armada. Si están trabados con algo (instalación, git, por dónde empezar), díganmelo en clase o por mensaje: es mejor preguntar que no subir nada.

**Próximos pasos (urgente)** — son los mismos del 24/09, con los nombres ya en inglés:
1. `main.py` mínimo que levante. Pruébenlo con `uvicorn main:app --reload` y abran `/docs`:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def home():
       return {"message": "HomeCome API"}
   ```
2. `db.py` con SQLAlchemy, siguiendo la [guía](guias/sqlalchemy_orm.md). Pueden copiar `guias/pokedex/db.py` y adaptarlo. Las tres tablas, en inglés:
   - `rooms`: id, name, floor
   - `devices`: id, name, type (light / sensor / lock / thermostat), status, `room_id` (FK)
   - `events`: id, date, description, `device_id` (FK)
3. `seed.py` que cargue unos 10 registros por tabla, solo si la base está vacía (sección 9 de la guía).
4. `requirements.txt` con `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.
5. Los dos primeros endpoints: `GET /devices?type=&status=` y `GET /devices/{id}` con 404.

Repártanse así: uno hace `db.py` y `seed.py`, el otro `main.py`. Suban cada paso apenas funcione, aunque sea chico.

## 08/10 — segunda revisión

**Lo que hay:** primer código del proyecto. 👍 Matías subió `main.py`, `seed.py` y `requirements.txt` (que está bien). `seed.py` define las tres tablas como clases de SQLAlchemy, con nombres de clase en inglés (`Room`, `Device`, `Event`), las claves foráneas y las relaciones. Lo probé y crea `homecore.db` con las tres tablas.

**⚠️ `main.py` no arranca.** Abre un archivo `datos.json` que no está en el repo, así que falla en la primera línea con `FileNotFoundError`. Y aunque el archivo estuviera, no es el camino: **los datos salen de la base**, no de un JSON. El endpoint tiene que consultar las tablas que crea el seed.

**⚠️ La API no tiene clave.** Es obligatoria en todos los endpoints. El código está arriba en *Seguridad*.

**⚠️ Christian sigue sin commits.** Tienen que aparecer los dos.

**A corregir en `seed.py`**
- Carga **una sola habitación** y ningún dispositivo ni evento. Se piden unos 10 registros por tabla.
- **Duplica los datos:** lo corrí dos veces y quedaron dos "Living". Tiene que cargar solo si la tabla está vacía (sección 9 de la [guía de SQLAlchemy](guias/sqlalchemy_orm.md)).
- **Tablas y columnas en inglés** (criterio nuevo): `rooms`, `devices`, `events`, con `name`, `floor`, `type`, `status`, `room_id`, `date`, `description`, `device_id`.
- Las clases y la conexión no van en el seed: van en `models.py`, y `seed.py` las importa. Está explicado en la guía nueva, [guias/estructura_del_proyecto.md](guias/estructura_del_proyecto.md).
- Usaron el estilo viejo de SQLAlchemy (`Column(Integer, ...)` y `declarative_base()`). Funciona, pero la guía usa el actual (`Mapped[int]` y `mapped_column`). Si siguen el de la guía, pueden copiar los ejemplos tal cual.
- `sessionmaker` y `check_same_thread` no hacen falta: alcanza con `with Session(engine) as s:`. Hoy la sesión `db` se abre y nunca se cierra.

**A corregir en `main.py`**
- Nombres en inglés: `obtener_dispositivos`, `archivo`, `datos` e `inicio` son funciones y variables de Python. La ruta también: `GET /devices`.
- El endpoint 1 lleva dos filtros opcionales: `GET /devices?type=light&status=on`.

**A corregir en el repo**
- `homecore.db` está subida. Agreguen `*.db` al `.gitignore` (hoy no la cubre) y sáquenla con `git rm --cached homecore.db`.
- El proyecto se llama **HomeCome** y la base y el mensaje de bienvenida dicen **HomeCore**. Elijan uno.
- El mensaje del commit es "new change". Tiene que decir qué se hizo.
- El README sigue con una línea. Hay una guía: [guias/como_escribir_un_readme.md](guias/como_escribir_un_readme.md).

**Próximos pasos**
1. Mover las tres clases y el `engine` a `models.py`, con tablas y columnas en inglés.
2. `seed.py` que importe de `models.py` y cargue ~10 habitaciones, ~10 dispositivos y ~10 eventos, solo si la base está vacía. Probar que corre dos veces sin duplicar.
3. `security.py` con la API key y probar el 401 en `/docs`.
4. `crud.py` con `list_devices(type, status)` y `get_device(device_id)`, y sus dos endpoints en `main.py`: `GET /devices` y `GET /devices/{id}` con 404.
5. Christian: tomá `security.py` y los endpoints. Tu primer commit tiene que aparecer esta semana.
