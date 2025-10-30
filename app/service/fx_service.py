from __future__ import annotations
from datetime import date
from decimal import Decimal
import os

class FXService:
    @staticmethod
    def get_a3500(fecha: date | None = None) -> tuple[Decimal, bool]:
        """
        Devuelve (tc_a3500, fue_fallback)
        MVP: usa solo fallback desde .env (A3500_FALLBACK) para no pegarle a la API todavía.
        """
        raw = os.getenv("A3500_FALLBACK", "1000.0")
        try:
            tc = Decimal(str(raw))
        except Exception:
            tc = Decimal("1000.0")
        return tc, True  # True indica que fue fallback (por ahora siempre)
