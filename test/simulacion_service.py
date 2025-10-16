import datetime
from app.models import Simulacion
from test.usuario_service import UsuarioServiceTest
from test.presupuesto_service import PresupuestoServiceTest

class SimulacionServiceTest:

    @staticmethod
    def simulacion_creation() -> Simulacion:
        simulacion=Simulacion()
        simulacion.usuario=UsuarioServiceTest.usuario_creation()
        simulacion.presupuesto=PresupuestoServiceTest.presupuesto_creation()
        simulacion.estado="activo"
        simulacion.num_escenario=1
        simulacion.fecha_creacion=datetime.datetime.now()
        simulacion.fecha_finalizacion=datetime.datetime.now()
        return simulacion
