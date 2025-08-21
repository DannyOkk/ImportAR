import unittest
import os
from flask import current_app
from app import create_app
from test.presupuesto_service import PresupuestoServiceTest

class SimulationTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_presupuesto_creation(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation()
        self.assertIsNotNone(presupuesto)
        self.assertEqual(presupuesto.estado, "finalizado")
        self.assertEqual(presupuesto.moneda, "USD")
        self.assertEqual(presupuesto.total, 1000.0)
        self.assertEqual(presupuesto.detalle, "Detalle del presupuesto")

if __name__ == '__main__':
    unittest.main()