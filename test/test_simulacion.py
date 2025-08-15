import unittest
import datetime
import os
from flask import current_app
from app import create_app
from app.models import Simulacion, Usuario

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
        simulacion.usuario=Usuario()
        simulacion.usuario.nombre = "Test User"
        simulacion.usuario.email = "test@example.com"
        simulacion.usuario.password = "securepassword"
        simulacion.usuario.rol = "admin"
        simulacion.usuario.plan = "basic"
        simulacion.usuario.fecha_alta = datetime.datetime.now()
        simulacion.estado="activo"
        simulacion.num_escenario=1
        simulacion.fecha_creacion=datetime.datetime.now()
        simulacion.fecha_finalizacion=datetime.datetime.now() 


if __name__ == '__main__':
    unittest.main()