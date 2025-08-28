import unittest
import os
from flask import current_app
from app import create_app, db
from test.usuario_service import UsuarioServiceTest
from app.service import UsuarioService

class UsuarioTest(unittest.TestCase):

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

    def test_usuario_creation(self):
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.id)
        self.assertGreater(usuario.id ,0)
        self.assertEqual(usuario.nombre, "Test User")
        self.assertEqual(usuario.email, "test@example.com")
        self.assertEqual(usuario.password_hash, "securepassword")
        self.assertEqual(usuario.rol, "admin")
        self.assertEqual(usuario.plan, "basic")

    def test_usuario_read(self):
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        fetched_usuario = UsuarioService.get_by_id(usuario.id)

        self.assertIsNotNone(fetched_usuario)
        self.assertEqual(fetched_usuario.id, usuario.id)
        self.assertEqual(fetched_usuario.nombre, "Test User")
        self.assertEqual(fetched_usuario.email, "test@example.com")
        self.assertEqual(usuario.password_hash, "securepassword")
        self.assertEqual(usuario.rol, "admin")
        self.assertEqual(usuario.plan, "basic")

    def test_usuario_read_all(self):
        usuario1 = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario1)

        usuario2 = UsuarioServiceTest.usuario_creation()
        usuario2.email = "test2@example.com"
        UsuarioService.create(usuario2)
        usuarios = UsuarioService.read_all()
        self.assertIsNotNone(usuarios)
        self.assertGreaterEqual(len(usuarios), 2)

if __name__ == '__main__':
    unittest.main()

