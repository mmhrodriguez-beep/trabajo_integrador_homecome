import json
from fastapi import FastAPI

app = FastAPI()

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


