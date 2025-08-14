import datetime
import unittest
import os
from flask import current_app
from app import create_app
from app.models import Usuario

class UsuarioTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_usuario_creation(self):
        usuario=Usuario()
        usuario.nombre = "Test User"
        usuario.email = "test@example.com"
        usuario.password = "securepassword"
        usuario.rol = "admin"
        usuario.plan = "basic"
        usuario.fecha_alta = datetime.datetime.now()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, "Test User")
        self.assertEqual(usuario.email, "test@example.com")
        self.assertEqual(usuario.password, "securepassword")
        self.assertEqual(usuario.rol, "admin")
        self.assertEqual(usuario.plan, "basic")

if __name__ == '__main__':
    unittest.main()