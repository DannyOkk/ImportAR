import unittest
import os
from flask import current_app
from app import create_app
from app.service import UsuarioService, EncrypterManager
from app.service.encrypter_service import PasslibEncrypterService, StandardEncrypterService
from test.usuario_service import UsuarioServiceTest

class EncryperTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_read_libpass(self):
        EncrypterManager.set_encrypter(PasslibEncrypterService)
        password_encrypted = EncrypterManager.hash_password("securepassword")
        self.assertIsNotNone(password_encrypted)
        self.assertNotEqual(password_encrypted, "securepassword")
        self.assertTrue(EncrypterManager.check_password(password_encrypted, "securepassword"))

    def test_read_standard(self):
        EncrypterManager.set_encrypter(StandardEncrypterService)
        password_encrypted = EncrypterManager.hash_password("securepassword")
        self.assertIsNotNone(password_encrypted)
        self.assertNotEqual(password_encrypted, "securepassword")
        self.assertTrue(EncrypterManager.check_password(password_encrypted, "securepassword"))

if __name__ == '__main__':
    unittest.main()

