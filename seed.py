from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Room(Base):
    __tablename__ = "habitaciones"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    piso = Column(Integer, nullable=False)

    devices = relationship("Device", back_populates="room")

class Device(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    habitacion_id = Column(
        Integer,
        ForeignKey("habitaciones.id"),
        nullable=False
    )
    room = relationship("Room", back_populates="devices")
    events = relationship("Event", back_populates="device")
    

class Event(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    dispositivo_id = Column(
        Integer,
        ForeignKey("dispositivos.id"),
        nullable=False
    )

    device = relationship("Device", back_populates="events")


DATABASE_URL = "sqlite:///homecore.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
db = SessionLocal()
living = Room(
    nombre="Living",
    piso=1
)
db.add(living)
db.commit()








