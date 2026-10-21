from models import Device
from sqlalchemy.orm import Session

def list_devices(db: Session, type: str | None = None, status: str | None = None):
    query = db.query(Device)

    if type is not None:
        query = query.filter(Device.type == type)

    if status is not None:
        query = query.filter(Device.status == status)
    return query.all()

def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()


def list_room_devices(db: Session, room_id: int):
    return db.query(Device).filter(Device.room_id == room_id).all()