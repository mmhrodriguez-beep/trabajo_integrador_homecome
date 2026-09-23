# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Matías Rodríguez Hrdy, Christian López
**Tema:** HomeCome — Casa inteligente

---

## 23/09

**Lo que hay:** README y `.gitignore`, sin código desde el 16/09.

**Sobre el tema:** aprobado. Como los datos de una casa son sensibles, todos los endpoints van con clave, igual que el resto de los grupos.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` con las 3 tablas: `habitaciones`, `dispositivos` (con `habitacion_id`) y `eventos` (con `dispositivo_id`).
3. Tipos de dispositivo sugeridos: luz, sensor, cerradura, termostato.

**Fuera de alcance:** dispositivos reales, hardware, MQTT y tiempo real. La API sirve datos, nada más.

**Endpoints a entregar (Nivel A)**
- [ ] `GET /dispositivos?tipo=luz&estado=encendido`
- [ ] `GET /dispositivos/{id}` (404 si no existe)
- [ ] `GET /habitaciones/{id}/dispositivos`
- [ ] `GET /eventos?dispositivo_id=3`
- [ ] `GET /resumen` (encendidos por habitación)
- [ ] `POST /dispositivos`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
