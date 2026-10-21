
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "clave-de-prueba-2026"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verification(clave: str = Depends(header)):
    if clave != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
