from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import TypedDict
import re
import unicodedata

from app.models import Presupuesto
from app.models.articulo import Articulo
from app.repositories import PresupuestoRepository
from app.service.apidolar_service import DolarApiService
from app.config.domain_constants import PESO_PROMEDIO_KG, TARIFA_USD_KG, PARAMS, DI_PCT

# Más precisión para impuestos
getcontext().prec = 28

# Mapa normalizado para lookup robusto de pesos
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

class PresupuestoService:
    @staticmethod
    def _decimal(n: float | int | str | Decimal) -> Decimal:
        return Decimal(str(n))

    @staticmethod
    def _round(v: Decimal, nd=2) -> Decimal:
        q = Decimal(10) ** -nd
        return v.quantize(q, rounding=ROUND_HALF_UP)

    @classmethod
    def calcular_cif(cls, dto: Articulo) -> tuple[Decimal, dict]:
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
    def calcular_impuestos(cls, cif: Decimal, origen: str, tipo_producto: str, es_courier: bool = False) -> ResultadoImpuesto:
        """
        Calcula los impuestos de importación.
        
        DI (Derecho de Importación):
        - Celulares con courier: 50%
        - Celulares sin courier: 8%
        - Notebooks: 0% (independiente de courier)
        """
        tipo_norm = tipo_producto.lower()
        
        # Determinar DI según tipo y courier
        if tipo_norm == "celulares":
            di_config = DI_PCT.get("celulares", {})
            di_pct = di_config.get("courier" if es_courier else "no_courier", Decimal("0"))
        elif tipo_norm == "notebooks":
            di_pct = DI_PCT.get("notebooks", Decimal("0"))
        else:
            di_pct = Decimal("0")
        
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
    def calcular(cls, dto: Articulo) -> Resultado:
        cif, flete_seguro = cls.calcular_cif(dto)
        imp_u = cls.calcular_impuestos(cif, dto.origen, dto.tipo_producto, dto.es_courier)
        costo_final_u = cif + sum(imp_u.values())

        tc, fue_fallback = DolarApiService.get_a3500()
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

    
