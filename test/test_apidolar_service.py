import unittest
import os
from decimal import Decimal
from app.service.apidolar_service import DolarApiService

class DolarApiServiceTest(unittest.TestCase):

    def setUp(self):
        # Guardar el valor original de A3500_FALLBACK
        self.original_fallback = os.getenv("A3500_FALLBACK")
        os.environ['A3500_FALLBACK'] = '1150.50'

    def tearDown(self):
        # Restaurar el valor original
        if self.original_fallback:
            os.environ['A3500_FALLBACK'] = self.original_fallback
        else:
            os.environ.pop('A3500_FALLBACK', None)

    def test_get_a3500_returns_decimal_and_bool(self):
        """Test: get_a3500 debe devolver una tupla (Decimal, bool)"""
        tc, fue_fallback = DolarApiService.get_a3500()
        
        self.assertIsInstance(tc, Decimal)
        self.assertIsInstance(fue_fallback, bool)
        self.assertGreater(tc, Decimal("0"))

    def test_fallback_cuando_api_falla(self):
        """Test: Si la API falla, debe usar el fallback de .env"""
        tc, fue_fallback = DolarApiService._get_fallback()
        
        self.assertEqual(tc, Decimal("1150.50"))
        self.assertTrue(fue_fallback)

    def test_fallback_con_valor_invalido(self):
        """Test: Si A3500_FALLBACK tiene valor inválido, usar 1000.0"""
        os.environ['A3500_FALLBACK'] = 'invalid'
        
        tc, fue_fallback = DolarApiService._get_fallback()
        
        self.assertEqual(tc, Decimal("1000.0"))
        self.assertTrue(fue_fallback)

    def test_get_a3500_integracion_real(self):
        """Test de integración: Llamar a la API real de dolarapi.com"""
        tc, fue_fallback = DolarApiService.get_a3500()
        
        # Verificar que obtuvimos un valor válido
        self.assertIsInstance(tc, Decimal)
        self.assertGreater(tc, Decimal("100"))  # TC razonable > 100
        self.assertLess(tc, Decimal("10000"))   # TC razonable < 10000
        
        self.assertIsInstance(fue_fallback, bool)
        
        if not fue_fallback:
            print(f"\nAPI dolarapi.com funcionando - TC: {tc}")
        else:
            print(f"\nUsando fallback - TC: {tc}")

if __name__ == '__main__':
    unittest.main()
