from dataclasses import dataclass
from app import db
from app.models.simulacion import Simulacion

@dataclass(init=False)
class Presupuesto(db.Model):
  
  __tablename__ = 'presupuestos'
  id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  estado: str = db.Column(db.String(50), nullable=False)
  moneda: str = db.Column(db.String(10), nullable=False)
  total: float = db.Column(db.Float, nullable=False)
  detalle: str = db.Column(db.Text, nullable=True)
