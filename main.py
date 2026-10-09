import json
from fastapi import FastAPI, Depends
from security import verification
from crud import get_cosas

app = FastAPI(dependencies=[Depends(verification)])


with open("datos.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a HOMECORE"
    }

@app.get("/dispositivos")
def obtener_dispositivos():
    return datos["dispositivos"]



#  `GET /cosas?campo=valor` | Query param, `select(...).where(...)` |
#  `GET /cosas/{id}` | Path param, **404** si no existe |
#  `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea (`relationship` o filtro por FK) |
#  `GET /otras?campo=valor` | Query param sobre otra tabla |
#  `GET /resumen` | Contar, sumar o agrupar (en Python o con `func` de SQLAlchemy) |
#  `POST /cosas` | Recibir el cuerpo como `dict`, **validar a mano** (400 si está mal) e insertar con la sesión |



@app.get("/cosas")
def obtener_dispositivos():
    data = get_cosas()
    # manejar la excepcion
    return data