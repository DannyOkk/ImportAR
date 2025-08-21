import unittest
import os
from flask import current_app
from app import create_app
from test.similacion_service import SimulacionServiceTest

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

    def test_simulation_creation(self):
        simulacion= SimulacionServiceTest.simulacion_creation()
        self.assertIsNotNone(simulacion)
        self.assertEqual(simulacion.estado, "activo")
        self.assertEqual(simulacion.num_escenario, 1)

if __name__ == '__main__':
    unittest.main()