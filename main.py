
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Room, Device, Event, engine
from security import verification
from crud import get_device, list_devices, list_room_devices

app = FastAPI(dependencies=[Depends(verification)])


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"mensaje": "Welcome to HOMECORE"}


@app.get("/devices")
def get_devices(
    type: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    try:
        devices = list_devices(db, type, status)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving devices"
        )


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


@app.get("/devices/{device_id}")
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db)
):
    try:
        device = get_device(db, device_id)
    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Database error while retrieving device"
    )

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
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving room"
        )

    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    devices = list_room_devices(db, room_id)

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
    try:
        query = db.query(Event)

        if device_id is not None:
            query = query.filter(Event.device_id == device_id)

        events = query.all()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving events"
        )

    return [
        {
            "id": event.id,
            "date": event.date,
            "description": event.description,
            "device_id": event.device_id
        }
        for event in events
    ]

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    try:
        rooms = db.query(Room).all()

        summary = [
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error while retrieving summary"
        )

    return summary
@app.post("/devices", status_code=201)
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

    if isinstance(data["room_id"], bool) or not isinstance(data["room_id"], int):
        raise HTTPException(
            status_code=400, 
            detail="room_id must be an integer"
        )   

    if not isinstance(data["name"], str):
       raise HTTPException(status_code=400, detail="Name must be a string")

    if not data["name"].strip():
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
