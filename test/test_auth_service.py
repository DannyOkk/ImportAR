import unittest
import os
from flask import current_app
from app import create_app, db
from app.service import AuthService, EncrypterManager
from app.models import Usuario


class AuthServiceTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_usuario_exitoso(self):
        """Test: Registrar un nuevo usuario correctamente"""
        usuario = AuthService.register(
            nombre="Test User",
            email="test@example.com",
            password="password123",
            rol="usuario",
            plan="básico"
        )
        
        self.assertIsNotNone(usuario)
        self.assertIsNotNone(usuario.id)
        self.assertEqual(usuario.nombre, "Test User")
        self.assertEqual(usuario.email, "test@example.com")
        self.assertEqual(usuario.rol, "usuario")
        self.assertEqual(usuario.plan, "básico")
        
        # Verificar que la contraseña fue hasheada
        self.assertNotEqual(usuario.password_hash, "password123")
        self.assertTrue(EncrypterManager.check_password(usuario.password_hash, "password123"))

    def test_register_email_duplicado(self):
        """Test: No se puede registrar un usuario con email duplicado"""
        # Registrar primer usuario
        AuthService.register(
            nombre="Usuario Uno",
            email="duplicado@example.com",
            password="password123"
        )
        
        # Intentar registrar otro con el mismo email
        with self.assertRaises(ValueError) as context:
            AuthService.register(
                nombre="Usuario Dos",
                email="duplicado@example.com",
                password="password456"
            )
        
        self.assertIn("email", str(context.exception).lower())
        self.assertIn("registrado", str(context.exception).lower())

    def test_login_exitoso(self):
        """Test: Login exitoso con credenciales correctas"""
        # Registrar usuario
        AuthService.register(
            nombre="Test User",
            email="login@example.com",
            password="password123"
        )
        
        # Intentar login
        usuario = AuthService.login("login@example.com", "password123")
        
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.email, "login@example.com")
        self.assertEqual(usuario.nombre, "Test User")

    def test_login_email_incorrecto(self):
        """Test: Login falla con email inexistente"""
        with self.assertRaises(ValueError) as context:
            AuthService.login("noexiste@example.com", "password123")
        
        self.assertIn("credenciales", str(context.exception).lower())

    def test_login_password_incorrecto(self):
        """Test: Login falla con contraseña incorrecta"""
        # Registrar usuario
        AuthService.register(
            nombre="Test User",
            email="test@example.com",
            password="password123"
        )
        
        # Intentar login con contraseña incorrecta
        with self.assertRaises(ValueError) as context:
            AuthService.login("test@example.com", "wrongpassword")
        
        self.assertIn("credenciales", str(context.exception).lower())

    def test_api_login_exitoso(self):
        """Test API: POST /api/v1/auth/login exitoso"""
        # Registrar usuario primero
        AuthService.register(
            nombre="API User",
            email="api@example.com",
            password="password123"
        )
        
        # Login via API
        response = self.client.post(
            '/api/v1/auth/login',
            json={
                "email": "api@example.com",
                "password": "password123"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "Login exitoso")
        self.assertIn('usuario', data['data'])
        self.assertEqual(data['data']['usuario']['email'], "api@example.com")

    def test_api_login_credenciales_invalidas(self):
        """Test API: POST /api/v1/auth/login con credenciales inválidas"""
        response = self.client.post(
            '/api/v1/auth/login',
            json={
                "email": "noexiste@example.com",
                "password": "wrongpassword"
            }
        )
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("credenciales", data['message'].lower())

    def test_api_register_exitoso(self):
        """Test API: POST /api/v1/auth/register exitoso"""
        response = self.client.post(
            '/api/v1/auth/register',
            json={
                "nombre": "New User",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], "Usuario registrado exitosamente")
        self.assertIn('usuario', data['data'])
        self.assertEqual(data['data']['usuario']['email'], "newuser@example.com")

    def test_api_register_email_duplicado(self):
        """Test API: POST /api/v1/auth/register con email duplicado"""
        # Registrar primer usuario
        self.client.post(
            '/api/v1/auth/register',
            json={
                "nombre": "User One",
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )
        
        # Intentar registrar con mismo email
        response = self.client.post(
            '/api/v1/auth/register',
            json={
                "nombre": "User Two",
                "email": "duplicate@example.com",
                "password": "password456"
            }
        )
        
        self.assertEqual(response.status_code, 409)
        data = response.get_json()
        self.assertIn("email", data['message'].lower())


if __name__ == '__main__':
    unittest.main()
