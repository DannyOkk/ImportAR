from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP, getcontext
from dataclasses import dataclass
from typing import Literal, TypedDict
from app.service.fx_service import FXService
import re
import unicodedata

# Más precisión para impuestos
getcontext().prec = 28

# Catálogos mínimos (MVP). Si querés, movemos a config o tablas.
TARIFA_USD_KG = {
    "US": Decimal("8.0"),
    "CN": Decimal("6.0"),
}
PESO_PROMEDIO_KG = {
    # Celulares (nuevas categorías)
    ("celulares", "ultra livianos"): Decimal("0.15"),
    ("celulares", "livianos estándar"): Decimal("0.20"),
    ("celulares", "peso medio"): Decimal("0.30"),
    ("celulares", "pesados/potentes"): Decimal("0.40"),
    ("celulares", "muy pesados/superphones"): Decimal("0.50"),
    # Notebooks (expandido)
    ("notebooks", "ultrabook"): Decimal("1.20"),
    ("notebooks", "convertible"): Decimal("1.50"),
    ("notebooks", "estandar/productividad"): Decimal("1.80"),
    ("notebooks", "gaming ligero"): Decimal("2.00"),
    ("notebooks", "gaming/alto rendimiento"): Decimal("2.70"),
    ("notebooks", "workstation/profesional"): Decimal("3.00"),
}

# Mapa normalizado para tolerar espacios/acentos/separadores en categoria_peso
def _norm_label(s: str) -> str:
    s = (s or "").strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[/\\\-]+", " ", s)
    s = ' '.join(s.split())
    s = s.lower()
    return s

PESO_PROMEDIO_KG_N = {
    (tipo, _norm_label(cat)): w for (tipo, cat), w in PESO_PROMEDIO_KG.items()
}
PARAMS = {
    "seguro_pct": Decimal("0.01"),      # 1% sobre FOB
    "tasa_est_pct": Decimal("0.03"),    # 3% sobre CIF
    "iva_pct": Decimal("0.21"),         # 21%
    "percep_iva_pct": Decimal("0.10"),  # 10% (parametrizable a 20%)
    "percep_gan_pct": Decimal("0.06"),  # 6%
}
# Derechos de Importación por origen y tipo_producto (MVP)
DI_PCT = {
    ("US", "celulares"): Decimal("0.00"),
    ("US", "notebooks"): Decimal("0.00"),
    ("CN", "celulares"): Decimal("0.00"),
    ("CN", "notebooks"): Decimal("0.00"),
}

class ResultadoImpuesto(TypedDict):
    di: Decimal
    tasa_est: Decimal
    iva: Decimal
    percep_iva: Decimal
    percep_gan: Decimal

class ResultadoUnitario(TypedDict):
    cif_usd: Decimal
    impuestos_usd: ResultadoImpuesto
    costo_final_usd: Decimal

class ResultadoTotal(TypedDict):
    impuestos_usd: ResultadoImpuesto
    costo_final_usd: Decimal
    costo_final_ars: Decimal

class Resultado(TypedDict):
    bases: dict
    unitario: ResultadoUnitario
    total: ResultadoTotal
    fuentes: dict

@dataclass
class ArticuloDTO:
    tipo_producto: str
    categoria_peso: str
    origen: str   # "US" | "CN"
    valor_usd: Decimal
    unidades: int
    modo_precio: Literal["CIF", "FOB"]

class CalculadoraService:
    @staticmethod
    def _decimal(n: float | int | str | Decimal) -> Decimal:
        return Decimal(str(n))

    @staticmethod
    def _round(v: Decimal, nd=2) -> Decimal:
        q = Decimal(10) ** -nd
        return v.quantize(q, rounding=ROUND_HALF_UP)

    @classmethod
    def calcular_cif(cls, dto: ArticuloDTO) -> tuple[Decimal, dict]:
        if dto.modo_precio.upper() == "CIF":
            cif = cls._decimal(dto.valor_usd)
            return cif, {"modo": "CIF"}
        # FOB
        fob = cls._decimal(dto.valor_usd)
        key_norm = (dto.tipo_producto.lower(), _norm_label(dto.categoria_peso))
        kg_prom = PESO_PROMEDIO_KG_N.get(key_norm, Decimal("0"))
        tarifa = TARIFA_USD_KG.get(dto.origen.upper(), Decimal("0"))
        flete = kg_prom * tarifa
        seguro = fob * PARAMS["seguro_pct"]
        cif = fob + flete + seguro
        return cif, {
            "modo": "FOB",
            "kg_promedio": str(cls._round(kg_prom, 3)),
            "tarifa_kg": str(cls._round(tarifa, 3)),
            "seguro_pct": str(PARAMS["seguro_pct"]),
            "flete": str(cls._round(flete)),
            "seguro": str(cls._round(seguro)),
        }

    @classmethod
    def calcular_impuestos(cls, cif: Decimal, origen: str, tipo_producto: str) -> ResultadoImpuesto:
        di_pct = DI_PCT.get((origen.upper(), tipo_producto.lower()), Decimal("0"))
        tasa_est_pct = PARAMS["tasa_est_pct"]
        iva_pct = PARAMS["iva_pct"]
        piva_pct = PARAMS["percep_iva_pct"]
        pgan_pct = PARAMS["percep_gan_pct"]

        di = cif * di_pct
        tasa_est = cif * tasa_est_pct
        base_iva = cif + di + tasa_est
        iva = base_iva * iva_pct
        percep_iva = base_iva * piva_pct
        percep_gan = cif * pgan_pct

        return {
            "di": cls._round(di),
            "tasa_est": cls._round(tasa_est),
            "iva": cls._round(iva),
            "percep_iva": cls._round(percep_iva),
            "percep_gan": cls._round(percep_gan),
        }

    @classmethod
    def calcular(cls, dto: ArticuloDTO) -> Resultado:
        cif, flete_seguro = cls.calcular_cif(dto)
        imp_u = cls.calcular_impuestos(cif, dto.origen, dto.tipo_producto)
        costo_final_u = cif + sum(imp_u.values())

        tc, fue_fallback = FXService.get_a3500()
        total_usd = cls._decimal(dto.unidades) * costo_final_u
        total_ars = total_usd * tc

        return {
            "bases": {
                "modo_precio": dto.modo_precio.upper(),
                "cif_unit_usd": str(cls._round(cif)),
                "origen": dto.origen.upper(),
                "tipo_producto": dto.tipo_producto.lower(),
                "categoria_peso": dto.categoria_peso.lower(),
                "unidades": dto.unidades,
                "tc_a3500": str(tc),
            },
            "unitario": {
                "cif_usd": str(cls._round(cif)),
                "impuestos_usd": {k: str(v) for k, v in imp_u.items()},
                "costo_final_usd": str(cls._round(costo_final_u)),
            },
            "total": {
                "impuestos_usd": {k: str(cls._round(v * dto.unidades)) for k, v in imp_u.items()},
                "costo_final_usd": str(cls._round(total_usd)),
                "costo_final_ars": str(cls._round(total_ars)),
            },
            "fuentes": {
                "fx": f"BCRA A3500 ({'fallback .env' if fue_fallback else 'oficial'})",
                "arancel": "Tabla interna (MVP)",
                "parametros": "Internos",
            },
        }
