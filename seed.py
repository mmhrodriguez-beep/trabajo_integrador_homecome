from models import Room, Device, Event, create_tables, engine
from sqlalchemy.orm import Session

def seed_database():
    create_tables()

    with Session(engine) as db:
        if db.query(Room).count() == 0:
            rooms = [
                Room(name="Living", floor=1),
                Room(name="Kitchen", floor=1),
                Room(name="Bedroom", floor=2),
                Room(name="Bathroom", floor=2),
                Room(name="Garage", floor=0),
                Room(name="Bedroom 2", floor=2),
                Room(name="Office", floor=1),
                Room(name="Dining Room", floor=1),
                Room(name="Patio", floor=0),
                Room(name="Laundy Room", floor=-1),

            ]
            db.add_all(rooms)
            db.commit()

    with Session(engine) as db:
        if db.query(Device).count() == 0:
            devices = [
                Device(name="Living Light", type="light", status="on", room_id=1),
                Device(name="Kitchen Light", type="light", status="off", room_id=2),
                Device(name="Motion Sensor", type="sensor", status="on", room_id=1),
                Device(name="Front Door Lock", type="lock", status="on", room_id=1),
                Device(name="Living Thermostat", type="thermostat", status="on", room_id=1),
                Device(name="Bedroom Light", type="light", status="off", room_id=3),
                Device(name="Garage Sensor", type="sensor", status="on", room_id=5),
                Device(name="Office Thermostat", type="thermostat", status="off", room_id=7),
                Device(name="Patio Light", type="light", status="on", room_id=10),  
                Device(name="Bedroom Lock", type="lock", status="on", room_id=6),

            ]  
            db.add_all(devices)
            db.commit()

        if db.query(Event).count() == 0:
            events = [
                Event(date="2026-10-01", description="Living light turned on", device_id=1),
                Event(date="2026-10-02", description="Kitchen light turned off", device_id=2),
                Event(date="2026-10-03", description="Motion detected", device_id=3),
                Event(date="2026-10-04", description="Front door locked", device_id=4),
                Event(date="2026-10-05", description="Thermostat activated", device_id=5),
                Event(date="2026-10-06", description="Bedroom light turned off", device_id=6),
                Event(date="2026-10-07", description="Garage motion detected", device_id=7),
                Event(date="2026-10-08", description="Office thermostat turned off", device_id=8),
                Event(date="2026-10-09", description="Patio light turned on", device_id=9),
                Event(date="2026-10-10", description="Bedroom door locked", device_id=10),
            ]
            db.add_all(events)
            db.commit()    


if __name__ == "__main__":
    seed_database()







