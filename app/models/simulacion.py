from dataclasses import dataclass
import datetime
from app.models.usuario import Usuario

@dataclass(init=False)
class Simulacion:
  usuario: Usuario
  estado: str
  num_escenario: int
  fecha_creacion: datetime
  fecha_finalizacion: datetime
