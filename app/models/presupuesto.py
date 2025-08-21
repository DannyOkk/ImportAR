from dataclasses import dataclass
from app.models.simulacion import Simulacion

@dataclass(init=False)
class Presupuesto:
  simulacion: Simulacion
  estado: str
  moneda: str
  total: float
  detalle: str