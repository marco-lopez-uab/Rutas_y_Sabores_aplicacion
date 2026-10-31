import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

class Cliente(Model):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    ci = Column(String(20), nullable=False, unique=True)
    telefono = Column(String(20))

    def __repr__(self):
        return f"{self.nombre} (CI: {self.ci})"


class Guia(Model):
    __tablename__ = 'guia'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(50))
    telefono = Column(String(20))

    def __repr__(self):
        return self.nombre


class Ruta(Model):
    __tablename__ = 'ruta'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    dificultad = Column(String(20))  # ej: Fácil, Media, Difícil
    duracion_horas = Column(Float)

    def __repr__(self):
        return self.nombre


class Refrigerio(Model):
    __tablename__ = 'refrigerio'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50))  # ej: Vegetariano, Tradicional, Energético
    descripcion = Column(Text)

    def __repr__(self):
        return self.nombre


class Excursion(Model):
    __tablename__ = 'excursion'
    id = Column(Integer, primary_key=True)
    fecha_salida = Column(Date, nullable=False, default=datetime.date.today)
    precio = Column(Float, nullable=False)

    # Claves foráneas (Relaciones 1 a N)
    ruta_id = Column(Integer, ForeignKey('ruta.id'), nullable=False)
    ruta = relationship("Ruta")

    guia_id = Column(Integer, ForeignKey('guia.id'), nullable=False)
    guia = relationship("Guia")

    refrigerio_id = Column(Integer, ForeignKey('refrigerio.id'), nullable=False)
    refrigerio = relationship("Refrigerio")

    def __repr__(self):
        return f"Excursión #{self.id} - {self.ruta} ({self.fecha_salida})"


class ReservaExcursion(Model):
    __tablename__ = 'reserva_excursion'
    id = Column(Integer, primary_key=True)
    fecha_reserva = Column(Date, nullable=False, default=datetime.date.today)
    num_personas = Column(Integer, default=1, nullable=False)

    # Claves foráneas (Relaciones 1 a N)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship("Cliente")

    excursion_id = Column(Integer, ForeignKey('excursion.id'), nullable=False)
    excursion = relationship("Excursion")

    def __repr__(self):
        return f"Reserva #{self.id} - {self.cliente}"

