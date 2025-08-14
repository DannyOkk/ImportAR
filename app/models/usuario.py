from dataclasses import dataclass
import datetime

@dataclass(init=False)
class Usuario:
  nombre: str
  email: str
  password_hash: str
  rol: str
  plan: str
  fecha_alta: datetime