from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Articulo:
    """
    Modelo de dominio para artículo a calcular.
    Usado como DTO único desde el schema hasta el servicio.
    """
    tipo_producto: str        
    categoria_peso: str       
    origen: str               
    valor_usd: Decimal        
    unidades: int             
    modo_precio: str = "FOB"  
    es_courier: bool = False  
