from __future__ import annotations
from datetime import date, datetime
from decimal import Decimal
import os
import requests
import urllib3

# Suprimir warnings de SSL solo para esta API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DolarApiService:
    # API alternativa más confiable: dolarapi.com (gratuita, sin autenticación)
    # Devuelve el dólar oficial del BCRA
    DOLAR_API_URL = "https://dolarapi.com/v1/dolares/oficial"
    
    # Backup: API del BCRA (puede tener problemas de SSL en algunos entornos)
    BCRA_API_URL = "https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/4"
    
    @staticmethod
    def get_a3500(fecha: date | None = None) -> tuple[Decimal, bool]:
        """
        Obtiene el tipo de cambio oficial (A3500) del dólar.
        
        Intenta primero con dolarapi.com (más confiable), luego BCRA, y finalmente fallback.
        
        Args:
            fecha: Fecha para la cual obtener el TC. Si es None, usa la última disponible.
                   Nota: dolarapi.com solo devuelve el valor actual, ignora fecha.
        
        Returns:
            tuple[Decimal, bool]: (tipo_cambio, fue_fallback)
            - tipo_cambio: El valor del TC oficial
            - fue_fallback: True si se usó el fallback de .env, False si vino de la API
        """
        # Primero intentar con dolarapi.com (más confiable)
        try:
            response = requests.get(
                DolarApiService.DOLAR_API_URL,
                timeout=5,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # dolarapi.com devuelve: {"compra": 1000, "venta": 1005, ...}
                # Usamos el precio de venta para importaciones
                if "venta" in data:
                    tc = Decimal(str(data["venta"]))
                    return tc, False
            
        except Exception:
            # Si falla dolarapi, continuar al siguiente método
            pass
        
        # Si dolarapi falló, intentar con BCRA (puede tener problemas SSL)
        if fecha:
            # Si se especificó fecha, usar API del BCRA con rango de fechas
            try:
                fecha_str = fecha.strftime("%Y-%m-%d")
                url = f"{DolarApiService.BCRA_API_URL}/{fecha_str}/{fecha_str}"
                
                response = requests.get(
                    url,
                    timeout=5,
                    headers={"Accept": "application/json"},
                    verify=False  # Desactivar verificación SSL para BCRA
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data and "results" in data and len(data["results"]) > 0:
                        tc = Decimal(str(data["results"][0]["valor"]))
                        return tc, False
                        
            except Exception:
                pass
        
        # Si todo falló, usar fallback
        return DolarApiService._get_fallback()
    
    @staticmethod
    def _get_fallback() -> tuple[Decimal, bool]:
        """
        Obtiene el tipo de cambio desde el fallback en .env
        
        Returns:
            tuple[Decimal, bool]: (tipo_cambio, True) - True indica que es fallback
        """
        raw = os.getenv("A3500_FALLBACK", "1000.0")
        try:
            tc = Decimal(str(raw))
        except Exception:
            tc = Decimal("1000.0")
        return tc, True
