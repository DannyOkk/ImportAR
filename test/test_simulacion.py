import unittest
import os
from flask import current_app
from app import create_app, db
from test.simulacion_service import SimulacionServiceTest
from app.service import SimulacionService

class SimulationTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_simulation_creation(self):
        simulacion= SimulacionServiceTest.simulacion_creation()
        SimulacionService.create(simulacion)
        self.assertIsNotNone(simulacion)
        self.assertEqual(simulacion.estado, "activo")
        self.assertEqual(simulacion.num_escenario, 1)

    def test_simulation_read(self):
        simulacion= SimulacionServiceTest.simulacion_creation()
        SimulacionService.create(simulacion)

        fetched_simulacion = SimulacionService.get_by_id(simulacion.id)

        self.assertIsNotNone(fetched_simulacion)
        self.assertEqual(fetched_simulacion.estado, "activo")
        self.assertEqual(fetched_simulacion.num_escenario, 1)

    def test_simulation_read_all(self):
        simulacion1= SimulacionServiceTest.simulacion_creation()
        SimulacionService.create(simulacion1)

        simulacion2= SimulacionServiceTest.simulacion_creation()
        simulacion2.usuario.email = "test2@example.com"
        simulacion2.num_escenario = 2
        SimulacionService.create(simulacion2)

        all_simulaciones = SimulacionService.read_all()

        self.assertIsNotNone(all_simulaciones)
        self.assertEqual(len(all_simulaciones), 2)
        self.assertEqual(all_simulaciones[0].num_escenario, 1)
        self.assertEqual(all_simulaciones[1].num_escenario, 2)

if __name__ == '__main__':
    unittest.main()