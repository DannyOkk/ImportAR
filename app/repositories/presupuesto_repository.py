from app.models import Presupuesto
from app import db
from app.repositories import Create, Read

class PresupuestoRepository(Create, Read):

    @staticmethod
    def create(presupuesto: Presupuesto) -> Presupuesto:
        if hasattr(presupuesto, "__table__"):
            db.session.add(presupuesto)
            db.session.commit()
            return presupuesto

        return presupuesto

    @staticmethod
    def get_by_id(id: int) -> Presupuesto:
        if hasattr(Presupuesto, "__table__"):
            return db.session.query(Presupuesto).filter_by(id=id).first()

        return None

    @staticmethod
    def read_all() -> list[Presupuesto]:
        if hasattr(Presupuesto, "__table__"):
            return db.session.query(Presupuesto).all()

        return []
