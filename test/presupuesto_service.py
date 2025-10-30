from app.models import Presupuesto
from app.models.articulo import Articulo
from decimal import Decimal

class PresupuestoServiceTest:

    @staticmethod
    def presupuesto_creation(usuario_id: int = 1) -> Presupuesto:        
        presupuesto = Presupuesto()
        presupuesto.usuario_id = usuario_id
        presupuesto.estado = "finalizado"
        presupuesto.moneda = "USD"
        presupuesto.total = 1000.0
        presupuesto.detalle = "Detalle del presupuesto"
        return presupuesto
    
    @staticmethod
    def articulo_celular_fob() -> Articulo:
        """Crea un artículo de celular en modo FOB para tests"""
        return Articulo(
            tipo_producto="celulares",
            categoria_peso="Peso medio",
            origen="US",
            valor_usd=Decimal("500.00"),
            unidades=2,
            modo_precio="FOB"
        )
    
    @staticmethod
    def articulo_notebook_cif() -> Articulo:
        """Crea un artículo de notebook en modo CIF para tests"""
        return Articulo(
            tipo_producto="notebooks",
            categoria_peso="Ultrabook",
            origen="CN",
            valor_usd=Decimal("800.00"),
            unidades=1,
            modo_precio="CIF"
        )