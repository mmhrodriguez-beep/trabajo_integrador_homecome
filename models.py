from sqlalchemy import create_engine, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_FILE = "homecore.db"
engine = create_engine(f"sqlite:///{DB_FILE}")

class Base(DeclarativeBase):
    pass

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    floor: Mapped[int]


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

# An event records something that happened to a device.
class Event(Base):          
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(200))
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))



def create_tables():
    Base.metadata.create_all(engine)





