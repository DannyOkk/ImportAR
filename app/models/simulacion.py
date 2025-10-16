from dataclasses import dataclass
import datetime
from app.models.usuario import Usuario
from app import db

@dataclass(init=False)
class Simulacion(db.Model):
  __tablename__ = 'simulaciones'

  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  usuario_id: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
  usuario = db.relationship('Usuario')
  presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'), nullable=False)  # Puede ser null si no se generó presupuesto
  presupuesto = db.relationship('Presupuesto', uselist=False)
  estado: str = db.Column(db.String(50), nullable=False)
  num_escenario: int = db.Column(db.Integer, nullable=False)
  fecha_creacion: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  fecha_finalizacion: datetime.datetime = db.Column(db.DateTime, nullable=True)
