from __future__ import annotations
from decimal import Decimal
import os
import requests

class DolarApiService:
    DOLAR_API_URL = "https://dolarapi.com/v1/dolares/oficial"
    
    DOLAR_MEP_URL = "https://dolarapi.com/v1/dolares/bolsa"

    @staticmethod
    def get_a3500() -> tuple[Decimal, bool]:
        """
        Obtiene el tipo de cambio oficial (A3500) del dólar desde dolarapi.com.
        Si la API falla, usa el fallback del .env.

        Returns:
            tuple[Decimal, bool]: (tipo_cambio, fue_fallback)
            - tipo_cambio: valor del TC oficial (venta)
            - fue_fallback: False si vino de la API, True si se usó fallback
        """
        try:
            response = requests.get(
                DolarApiService.DOLAR_API_URL,
                timeout=5,
                headers={"Accept": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                if "venta" in data:
                    tc = Decimal(str(data["venta"]))
                    return tc, False
        except Exception:
            pass

        return DolarApiService._get_fallback()
    
    @staticmethod
    def get_mep() -> tuple[Decimal, bool]:
        """
        Obtiene el tipo de cambio MEP (Mercado Electrónico de Pagos / Dólar Bolsa).
        
        Returns:
            tuple[Decimal, bool]: (tipo_cambio_mep, fue_fallback)
            - tipo_cambio_mep: El valor del dólar MEP
            - fue_fallback: True si se usó el fallback, False si vino de la API
        """
        try:
            response = requests.get(
                DolarApiService.DOLAR_MEP_URL,
                timeout=5,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "venta" in data:
                    tc_mep = Decimal(str(data["venta"]))
                    return tc_mep, False
            
        except Exception:
            pass
        raw = os.getenv("MEP_FALLBACK", "1500.0")
        try:
            tc_mep = Decimal(str(raw))
        except Exception:
            tc_mep = Decimal("1500.0")
        return tc_mep, True
    
    @staticmethod
    def _get_fallback() -> tuple[Decimal, bool]:
        """
        Lee el valor de respaldo desde la variable de entorno A3500_FALLBACK.
        Si no está definida, usa 1000.0 por defecto.
        """
        raw = os.getenv("A3500_FALLBACK", "1000.0")
        try:
            tc = Decimal(str(raw))
        except Exception:
            tc = Decimal("1000.0")
        return tc, True
