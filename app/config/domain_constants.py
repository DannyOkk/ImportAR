"""
Constantes de dominio: tipos, categorías, pesos, tarifas y parámetros de impuestos.
Centralizado para evitar duplicación entre schema y servicio.
"""
from decimal import Decimal

# Tipos de producto permitidos
TIPOS = ["celulares", "notebooks"]

# Categorías por tipo de producto
CATEGORIAS = {
    "celulares": [
        "Ultra livianos",
        "Livianos estándar",
        "Peso medio",
        "Pesados/Potentes",
        "Muy pesados/Superphones"
    ],
    "notebooks": [
        "Ultrabook",
        "Convertible",
        "Estandar/Productividad",
        "Gaming ligero",
        "Gaming/Alto rendimiento",
        "Workstation/Profesional"
    ],
}

# Peso promedio por categoría (kg) para cálculo de flete
PESO_PROMEDIO_KG = {
    # Celulares
    ("celulares", "ultra livianos"): Decimal("0.125"),
    ("celulares", "livianos estándar"): Decimal("0.160"),
    ("celulares", "peso medio"): Decimal("0.185"),
    ("celulares", "pesados/potentes"): Decimal("0.230"),
    ("celulares", "muy pesados/superphones"): Decimal("0.3"),
    # Notebooks
    ("notebooks", "ultrabook"): Decimal("1.25"),
    ("notebooks", "convertible"): Decimal("1.40"),
    ("notebooks", "estandar/productividad"): Decimal("1.90"),
    ("notebooks", "gaming ligero"): Decimal("2.15"),
    ("notebooks", "gaming/alto rendimiento"): Decimal("2.65"),
    ("notebooks", "workstation/profesional"): Decimal("3.00"),
}

# Tarifa de flete por kg según origen
TARIFA_USD_KG = {
    "US": Decimal("17.0"),
    "CN": Decimal("7.0"),
}

# Parámetros de cálculo de impuestos (porcentajes)
PARAMS = {
    "seguro_pct": Decimal("0.02"),      # 2% sobre FOB
    "iva_pct": Decimal("0.21"),         # 21%
    "percep_iva_pct": Decimal("0.20"),  # 20%
    "percep_gan_pct": Decimal("0.06"),  # 6%
    "tasa_est_pct": Decimal("0.03"),    # 3% sobre CIF (tasa de estadística)
}

# Derechos de Importación (DI) por tipo de producto y courier
# Para celulares: depende si es courier (50%) o no (8%)
# Para notebooks: siempre 0%
DI_PCT = {
    "celulares": {
        "courier": Decimal("0.50"),      # 50% si viene por courier
        "no_courier": Decimal("0.08"),   # 8% si no es courier
    },
    "notebooks": Decimal("0.00"),        # 0% siempre para notebooks
}
