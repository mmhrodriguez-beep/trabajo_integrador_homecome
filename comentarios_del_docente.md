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
- Datos en **SQLite**. Pueden usar **SQLAlchemy** (ORM, con la guía [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)) o **`sqlite3` con SQL directo**: las dos formas valen. **Pydantic es opcional**: el cuerpo del `POST` se puede validar con un modelo de Pydantic (`class StudentIn(BaseModel)`) o a mano en `validation.py`. Las dos formas valen.
- Repositorio en GitHub con commits de **todos** los integrantes.
- **Demo local:** la API se corre en la notebook de cada grupo con `uvicorn`. No hace falta desplegarla en la web (ver *Demo local*, abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 15/10:** los nombres de tablas, columnas y rutas en inglés pasan a ser una **recomendación**. Si quedan en español, no es un error.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params:** se recomienda que también vayan en inglés (`__tablename__ = "students"`, columna `career_id`, ruta `GET /students`), pero pueden quedar en español, como figuran en el alcance.
- Lo que sí es obligatorio: usar **el mismo nombre en todos los archivos** (`models.py`, `seed.py`, `crud.py`, `main.py`, `validation.py`). Si la tabla se llama `estudiantes` en el seed, se llama `estudiantes` en todos lados.
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Demo local (sin despliegue)

> **Actualizado el 15/10:** no se despliega a producción. La defensa es **local**, en la notebook del grupo.

`requirements.txt` debe incluir:
```
fastapi
uvicorn
python-dotenv
```
y `sqlalchemy` si lo usan.

Para levantar el proyecto desde cero (lo mismo tiene que estar en el README):
```
python -m venv venv
venv\Scripts\activate          (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```
Y abrir http://127.0.0.1:8000/docs.

- El seed se corre **una vez, antes** de levantar el servidor. No va adentro de `main.py`.
- Antes de la defensa, prueben todo esto en la notebook con la que van a presentar.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- **Algunos datos de ejemplo** en cada tabla, los suficientes para ver funcionar los endpoints. No hay mínimo ni máximo. Siempre **datos ficticios**.
- Recomendación: que los datos permitan ver los filtros en acción, por ejemplo productos de varias categorías, para que `?category=` devuelva algo distinto de la lista completa.
- Un script de carga inicial `seed.py` que crea las tablas (con `create_all` o con `CREATE TABLE IF NOT EXISTS`) y carga los datos **solo si la base está vacía**. Se ejecuta antes de levantar el servidor y, si se corre dos veces, no duplica nada.
- El archivo `.db` **puede estar en el repo**. Si lo suben, que esté actualizado (el que genera el seed actual).

### Seguridad: TODOS los endpoints van protegidos

> **Actualizado el 15/10:** se **recomienda** guardar la clave en una variable de entorno en lugar de escribirla en el código. No es obligatorio; en la defensa se puede preguntar por qué conviene hacerlo.

- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- Sin clave o con clave incorrecta → **401**. Con la clave correcta → **200** y los datos.
- **Recomendado:** guardar la clave en un archivo **`.env`** que **no se sube** (va en el `.gitignore`) y leerla con `python-dotenv`. Al repo se sube un **`.env.example`** con el nombre de la variable y sin el valor. Paso a paso en [guias/variables_de_entorno.md](guias/variables_de_entorno.md). Si la dejan como constante en `security.py`, también vale.
- Los datos son todos **ficticios**: esta API no se usa para nada real.

`security.py` con la clave en el `.env` (la forma recomendada):

```python
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Y en `main.py` se protege toda la app de una vez:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.
---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param y filtro en la consulta |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o en la consulta) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo (con un modelo de Pydantic o como `dict` validado a mano), rechazar los datos inválidos con **400** o **422**, e insertar en la base |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Seguridad (recomendado):** API key en variable de entorno (`.env`) en lugar de escrita en el código.
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
2. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
3. Defensa oral el **miércoles 28/10**: demo en vivo desde `/docs`, en local, y preguntas sobre el código. El repositorio tiene que estar al día el **miércoles 21/10**.

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

## 15/10

**📌 Cambios en las reglas** (están arriba, en *Reglas comunes*):
- **SQLAlchemy es opcional:** también vale `sqlite3` con SQL directo.
- **No hay que desplegar.** La defensa es **local**, en su notebook, el **miércoles 28/10**. El repo tiene que estar al día el **miércoles 21/10**.
- **Recomendado:** la API key en una variable de entorno (`.env`) en lugar de escrita en el código. No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Lo que hay:** el avance más grande de la semana, y de los dos. 👍 Probé la API y **los cinco GET funcionan**, con sus filtros y sus 404: `GET /devices?type=&status=`, `GET /devices/{id}`, `GET /rooms/{id}/devices`, `GET /events?device_id=` y `GET /summary` (los números coinciden con el seed). El seed carga 10 + 10 + 10 y no duplica. Sin clave o con clave mala da 401. Tablas, columnas y rutas en inglés. El `POST /devices` valida a mano y devuelve 400 en la mayoría de los casos.

**Están cerca. Lo que falta para la entrega del 21/10:**

1. **README.** Hoy tiene una línea. Tiene que decir qué hace la API, los endpoints, cómo usar la clave, cómo correrla desde cero y si usaron IA. Hay una guía con una plantilla: [guias/como_escribir_un_readme.md](guias/como_escribir_un_readme.md).
2. **`try/except` en las consultas.** Si falta la base, todos los endpoints dan 500 sin control. Pasa también si alguien clona el repo y no corre el seed, porque el `homecore.db` que está subido es el viejo, con las tablas en español. Pueden dejarla en el repo, pero súbanla actualizada: corran el seed y commiteen la base nueva.
3. **Arreglos en el `POST /devices`:**
   - `"room_id": true` se acepta y se guarda como 1. Descarten los booleanos con `isinstance(room_id, bool)`.
   - `"name": 123` da 500: falta controlar que sea texto antes del `.strip()`.
   - El seed carga cerraduras con `status="locked"`, pero el `POST` solo acepta `on` y `off`. Unifiquen los valores.
   - Un alta tiene que devolver **201**: `@app.post("/devices", status_code=201)`.

**Recomendación:** pasar la clave a un `.env` (ver *Seguridad*, arriba, y [guias/variables_de_entorno.md](guias/variables_de_entorno.md)). No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Más chico:**
- `main.py` no usa `crud.py`: todas las consultas siguen en los endpoints, y las dos funciones de `crud.py` no se llaman desde ningún lado. Lo ideal es moverlas (ver [guias/estructura_del_proyecto.md](guias/estructura_del_proyecto.md)). Si no llegan, borren `crud.py` para que no quede código muerto. En la defensa les pueden preguntar por qué está.
- Quedan cosas en español: `inicio`, `"mensaje"`, `CLAVE`, `clave` y "API key invalida".
- "Living Thermostrat" en el seed está mal escrito.

## 21/10 (entrega)

**Lo que hay:** sin cambios desde el **14/10**. El estado es el que describí el 15/10: los cinco GET funcionan, con sus filtros, sus 404 y la clave (401), y el `POST /devices` valida casi todo.

**Lo que quedó pendiente para la defensa (28/10)**, en orden de importancia:
1. **README.** Sigue con una línea. En la defensa se evalúa que explique cómo correr el proyecto desde cero, los endpoints y cómo usar la clave. Hay una plantilla en [guias/como_escribir_un_readme.md](guias/como_escribir_un_readme.md).
2. **`try/except` en las consultas.** Sin la base, todos los endpoints dan 500 sin control.
3. **El `POST /devices`:**
   - acepta `"room_id": true`;
   - da 500 con `"name": 123`;
   - rechaza el `status="locked"` que carga el propio seed;
   - responde 200 en lugar de 201.

**Para la defensa:** probá la demo completa en la notebook con la que van a presentar. Corran `python seed.py` antes de levantar: el `homecore.db` subido al repo es el viejo, y sin el seed la API da 500. La nota es grupal: los dos tienen que poder explicar cualquier parte del código.
