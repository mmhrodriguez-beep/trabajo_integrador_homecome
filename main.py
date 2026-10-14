
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Room, Device, Event, engine
from security import verification

app = FastAPI(dependencies=[Depends(verification)])


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def inicio():
    return {"mensaje": "Welcome to HOMECORE"}


@app.get("/devices")
def get_devices(
    type: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Device)

    if type is not None:
        query = query.filter(Device.type == type)

    if status is not None:
        query = query.filter(Device.status == status)

    return [
        {
            "id": device.id,
            "name": device.name,
            "type": device.type,
            "status": device.status,
            "room_id": device.room_id
        }
        for device in query.all()
    ]


@app.get("/devices/{device_id}")
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "status": device.status,
        "room_id": device.room_id
    }

@app.get("/rooms/{room_id}/devices")
def get_room_devices(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    devices = db.query(Device).filter(Device.room_id == room_id).all()

    return [
        {
            "id": device.id,
            "name": device.name,
            "type": device.type,
            "status": device.status,
            "room_id": device.room_id
        }
        for device in devices
    ]

@app.get("/events")
def get_events(
    device_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if device_id is not None:
        query = query.filter(Event.device_id == device_id)

    return [
        {
            "id": event.id,
            "date": event.date,
            "description": event.description,
            "device_id": event.device_id
        }
        for event in query.all()
    ]

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()

    return [
        {
            "room_id": room.id,
            "room_name": room.name,
            "devices_on": db.query(Device).filter(
                Device.room_id == room.id,
                Device.status == "on"
            ).count()
        }
        for room in rooms
    ]

@app.post("/devices")
def create_device(data: dict, db: Session = Depends(get_db)):
    required_fields =  ["name", "type", "status", "room_id"]

    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing field: {field}"
            )

    if data["type"] not in ["light", "sensor", "lock", "thermostat"]:
        raise HTTPException(status_code=400, detail="Invalid device type")


    if data["status"] not in ["on", "off"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid device status"
        )

    if not isinstance(data["room_id"], int):
        raise HTTPException(
            status_code=400, 
            detail="room_id must be an integer"
        )   

    if not data ["name"].strip():
        raise HTTPException(
            status_code=400,    
            detail="Name cannot be empty"
        )

    room = db.query(Room).filter(Room.id == data["room_id"]).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    device = Device(
        name=data["name"],
        type=data["type"],
        status=data["status"],
        room_id=data["room_id"]
    )

    try:
        db.add(device)
        db.commit()
        db.refresh(device)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create device")

    return {
        "id": device.id,
        "name": device.name,
        "type": device.type,
        "status": device.status,
        "room_id": device.room_id
    }
