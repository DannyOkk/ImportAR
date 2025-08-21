from app.models import Presupuesto
from test.simulacion_service import SimulacionServiceTest

class PresupuestoServiceTest:

    @staticmethod
    def presupuesto_creation() -> Presupuesto:        
        presupuesto = Presupuesto()
        presupuesto.simulacion = SimulacionServiceTest.simulacion_creation()
        presupuesto.estado = "finalizado"
        presupuesto.moneda = "USD"
        presupuesto.total = 1000.0
        presupuesto.detalle = "Detalle del presupuesto"
        return presupuesto