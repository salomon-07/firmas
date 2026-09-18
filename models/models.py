from extensions import db
from datetime import datetime

class Constancia(db.Model):
    __tablename__ = 'constancias'

    id = db.Column(db.Integer, primary_key=True)
    # Datos del Colaborador
    nombre = db.Column(db.String(150), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    puesto = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    plaza = db.Column(db.String(50), nullable=False)

    # Datos de IT
    gerencia = db.Column(db.String(100), default='Gerencia IT')
    sitio = db.Column(db.String(50), nullable=False)
    tecnico = db.Column(db.String(100), nullable=False)
    asunto = db.Column(db.String(100), default='Entrega de equipo')
    licencia = db.Column(db.String(50), default='Básica')

    # Entrega y Recepción
    nombre_entrega = db.Column(db.String(100), nullable=False)
    firma_base64 = db.Column(db.Text, nullable=True) # Imagen de la firma grabada

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con items/equipos
    equipos = db.relationship('EquipoItem', backref='constancia', cascade="all, delete-orphan", lazy=True)


class EquipoItem(db.Model):
    __tablename__ = 'equipos_items'

    id = db.Column(db.Integer, primary_key=True)
    constancia_id = db.Column(db.Integer, db.ForeignKey('constancias.id'), nullable=False)
    equipo = db.Column(db.String(100), nullable=False) # ej: Laptop, Cargador
    marca = db.Column(db.String(100), nullable=False)  # ej: DELL
    modelo = db.Column(db.String(100), nullable=False) # ej: LATITUDE 3420
    serie = db.Column(db.String(100), nullable=False)  # ej: DT6VGL3
    estado = db.Column(db.String(50), nullable=False)  # ej: usada, nueva