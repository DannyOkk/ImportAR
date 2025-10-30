from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Articulo:
    """
    Modelo de dominio para artículo a calcular.
    Usado como DTO único desde el schema hasta el servicio.
    """
    tipo_producto: str        # "celulares" | "notebooks"
    categoria_peso: str       # Según tipo (ver domain_constants.CATEGORIAS)
    origen: str               # "US" | "CN"
    valor_usd: Decimal        # CIF o FOB según modo_precio
    unidades: int             # >= 1
    modo_precio: str = "FOB"  # "CIF" | "FOB"
    es_courier: bool = False  # True si viene por courier (afecta DI en celulares)
