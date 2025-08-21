import unittest
import datetime
import os
from flask import current_app
from app import create_app
from app.models import Simulacion, Usuario
from test.usuario_service import UsuarioServiceTest

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
        simulacion=Simulacion()
        #TODO: Refactorizarlo a un archivo separado
        simulacion.usuario=UsuarioServiceTest.usuario_creation()
        simulacion.estado="activo"
        simulacion.num_escenario=1
        simulacion.fecha_creacion=datetime.datetime.now()
        simulacion.fecha_finalizacion=datetime.datetime.now() 
        self.assertIsNotNone(simulacion)
        self.assertEqual(simulacion.estado, "activo")
        self.assertEqual(simulacion.num_escenario, 1)

if __name__ == '__main__':
    unittest.main()