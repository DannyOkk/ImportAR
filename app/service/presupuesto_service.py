from app.models import Presupuesto
from app.repositories import PresupuestoRepository

class PresupuestoService:
    @staticmethod
    def create(presupuesto: Presupuesto) -> Presupuesto:
        """Create a new presupuesto using the repository and return it."""
        PresupuestoRepository.create(presupuesto)
        return presupuesto

    @staticmethod
    def get_by_id(id: int) -> Presupuesto:
        return PresupuestoRepository.get_by_id(id)

    @staticmethod
    def read_all() -> list[Presupuesto]:
        return PresupuestoRepository.read_all()
