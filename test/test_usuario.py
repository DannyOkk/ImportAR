import unittest
import os
from flask import current_app
from app import create_app, db
from app.service import UsuarioService, EncrypterManager
from test.usuario_service import UsuarioServiceTest


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
        self.assertNotEqual(usuario.password_hash, "securepassword")
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
        self.assertNotEqual(usuario.password_hash, "securepassword")
        self.assertTrue(EncrypterManager.check_password(usuario.password_hash, "securepassword"))
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

    def test_usuario_update(self):
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        updated_usuario = UsuarioService.get_by_id(usuario.id)

        usuario.nombre = "Updated User"
        updated_usuario = UsuarioService.update(usuario, usuario.id)
        
        self.assertIsNotNone(updated_usuario)
        self.assertEqual(updated_usuario.nombre, "Updated User")

    def test_usuario_delete(self):
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        deleted_usuario = UsuarioService.delete(usuario.id)

        self.assertTrue(deleted_usuario)
    

if __name__ == '__main__':
    unittest.main()

