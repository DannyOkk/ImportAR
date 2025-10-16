from app.models import Presupuesto

class PresupuestoServiceTest:

    @staticmethod
    def presupuesto_creation() -> Presupuesto:        
        presupuesto = Presupuesto()
        presupuesto.estado = "finalizado"
        presupuesto.moneda = "USD"
        presupuesto.total = 1000.0
        presupuesto.detalle = "Detalle del presupuesto"
        return presupuesto