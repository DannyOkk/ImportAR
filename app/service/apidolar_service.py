from __future__ import annotations
from decimal import Decimal
import os
import requests

class DolarApiService:
    # API principal (única): dolarapi.com
    DOLAR_API_URL = "https://dolarapi.com/v1/dolares/oficial"

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
                # dolarapi.com devuelve {"compra": ..., "venta": ..., ...}
                if "venta" in data:
                    tc = Decimal(str(data["venta"]))
                    return tc, False
        except Exception:
            # si algo explota (timeout, etc.), cae al fallback
            pass

        # fallback si la API no respondió bien
        return DolarApiService._get_fallback()

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
