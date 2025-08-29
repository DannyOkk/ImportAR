from app.models import Simulacion
from app import db
from typing import List

class SimulacionRepository: 

    @staticmethod
    def create(simulacion: Simulacion) -> Simulacion:
        db.session.add(simulacion)
        db.session.commit()
        return simulacion

    @staticmethod
    def get_by_id(id: int) -> Simulacion:

        return db.session.query(Simulacion).filter_by(id=id).first()
    
    @staticmethod
    def read_all() -> list[Simulacion]:
        return db.session.query(Simulacion).all()