from dataclasses import dataclass
import datetime
from app import db

@dataclass(init=False)
class Usuario(db.Model): 
  __tablename__ = 'usuarios'

  id: int= db.Column(db.Integer, primary_key=True, autoincrement=True)
  nombre: str= db.Column(db.String(100), nullable=False)
  email: str= db.Column(db.String(120), unique=True, nullable=False)
  password_hash: str= db.Column(db.String(255), nullable=False)
  rol: str= db.Column(db.String(50), nullable=False)
  plan: str= db.Column(db.String(120), nullable=False)
  fecha_alta: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  
