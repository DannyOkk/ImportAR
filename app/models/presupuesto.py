from dataclasses import dataclass
from app import db

@dataclass(init=False)
class Presupuesto(db.Model):
  
  __tablename__ = 'presupuestos'
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  usuario_id: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
  usuario = db.relationship('Usuario')
  total: float = db.Column(db.Float, nullable=False)
