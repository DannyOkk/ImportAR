import unittest
import os
import json
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
        self.client = self.app.test_client()

        
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

    def test_usuario_update_password_changes(self):
        # Crear usuario inicial con password en texto plano (se hashea en create)
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        # Guardar el hash anterior
        old_hash = usuario.password_hash
        self.assertTrue(EncrypterManager.check_password(old_hash, "securepassword"))

        # Actualizar con una nueva contraseña en texto plano
        usuario.password_hash = "new_secure_password"
        updated = UsuarioService.update(usuario, usuario.id)

        # Traer de BD y verificar que cambió el hash y valida solo la nueva
        fetched = UsuarioService.get_by_id(usuario.id)
        self.assertIsNotNone(fetched)
        self.assertNotEqual(fetched.password_hash, old_hash)
        self.assertTrue(EncrypterManager.check_password(fetched.password_hash, "new_secure_password"))
        self.assertFalse(EncrypterManager.check_password(fetched.password_hash, "securepassword"))

    def test_usuario_delete(self):
        usuario = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario)

        deleted_usuario = UsuarioService.delete(usuario.id)

        self.assertTrue(deleted_usuario)
    
    def test_usuario_email_duplicado(self):
        """Test: No se puede crear usuario con email duplicado"""
        usuario1 = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario1)

        # Intentar crear otro usuario con el mismo email
        usuario2 = UsuarioServiceTest.usuario_creation()
        
        with self.assertRaises(ValueError) as context:
            UsuarioService.create(usuario2)
        
        self.assertIn("email", str(context.exception).lower())
        self.assertIn("registrado", str(context.exception).lower())

    # ==================== TESTS DE API (Issue #11) ====================

    def test_api_post_crear_usuario_exitoso(self):
        """
        Test API: Registrar un nuevo usuario con datos válidos.
        Endpoint: POST /api/v1/usuarios/
        Resultado esperado: 201 Created
        """
        nuevo_usuario = {
            "nombre": "Juan Pérez",
            "email": "juan.perez@example.com",
            "password_hash": "password123",
            "rol": "usuario",
            "plan": "básico"
        }

        response = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(nuevo_usuario),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Usuario creado en el sistema")
        self.assertEqual(data['status_code'], 201)

        # Verificar que el usuario fue creado en la base de datos
        usuarios = UsuarioService.read_all()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].email, "juan.perez@example.com")

    def test_api_post_crear_usuario_email_duplicado(self):
        """
        Test API: Intentar registrar un usuario con email duplicado.
        Endpoint: POST /api/v1/usuarios/
        Resultado esperado: 409 Conflict
        """
        usuario_data = {
            "nombre": "Usuario Uno",
            "email": "duplicado@example.com",
            "password_hash": "password123",
            "rol": "usuario",
            "plan": "básico"
        }

        # Primer registro - debe ser exitoso
        response1 = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(usuario_data),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 201)

        # Segundo registro con el mismo email - debe fallar
        response2 = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(usuario_data),
            content_type='application/json'
        )
        
        self.assertEqual(response2.status_code, 409)
        data = json.loads(response2.data)
        self.assertIn("email", data['message'].lower())

    def test_api_post_crear_usuario_sin_email(self):
        """
        Test API: Intentar registrar un usuario sin email.
        Endpoint: POST /api/v1/usuarios/
        Resultado esperado: 400 Bad Request
        """
        usuario_sin_email = {
            "nombre": "Usuario Sin Email",
            "password_hash": "password123",
            "rol": "usuario",
            "plan": "básico"
        }

        response = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(usuario_sin_email),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_api_post_crear_usuario_sin_password(self):
        """
        Test API: Intentar registrar un usuario sin contraseña.
        Endpoint: POST /api/v1/usuarios/
        Resultado esperado: 400 Bad Request
        """
        usuario_sin_password = {
            "nombre": "Usuario Sin Password",
            "email": "sinpassword@example.com",
            "rol": "usuario",
            "plan": "básico"
        }

        response = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(usuario_sin_password),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_api_post_crear_usuario_email_invalido(self):
        """
        Test API: Intentar registrar un usuario con email mal formado.
        Endpoint: POST /api/v1/usuarios/
        Resultado esperado: 400 Bad Request
        """
        usuario_email_invalido = {
            "nombre": "Usuario Email Inválido",
            "email": "email-invalido",
            "password_hash": "password123",
            "rol": "usuario",
            "plan": "básico"
        }

        response = self.client.post(
            '/api/v1/usuarios/',
            data=json.dumps(usuario_email_invalido),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_api_get_listar_todos_usuarios(self):
        """
        Test API: Obtener lista de todos los usuarios.
        Endpoint: GET /api/v1/usuarios/
        Resultado esperado: 200 OK con lista de usuarios
        """
        # Crear algunos usuarios de prueba
        usuario1 = UsuarioServiceTest.usuario_creation()
        UsuarioService.create(usuario1)

        usuario2 = UsuarioServiceTest.usuario_creation()
        usuario2.email = "test2@example.com"
        UsuarioService.create(usuario2)

        response = self.client.get('/api/v1/usuarios/')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_api_get_usuario_por_id_existente(self):
        """
        Test API: Obtener un usuario específico por ID.
        Endpoint: GET /api/v1/usuarios/<id>
        Resultado esperado: 200 OK con datos del usuario
        """
        # Crear un usuario de prueba
        usuario = UsuarioServiceTest.usuario_creation()
        usuario_creado = UsuarioService.create(usuario)

        response = self.client.get(f'/api/v1/usuarios/{usuario_creado.id}')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Usuario encontrado")
        self.assertEqual(data['data']['email'], "test@example.com")

    def test_api_get_usuario_por_id_no_existente(self):
        """
        Test API: Intentar obtener un usuario con ID inexistente.
        Endpoint: GET /api/v1/usuarios/<id>
        Resultado esperado: 404 Not Found
        """
        response = self.client.get('/api/v1/usuarios/9999')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Usuario no encontrado")

    def test_api_put_actualizar_usuario_existente(self):
        """
        Test API: Actualizar datos de un usuario existente.
        Endpoint: PUT /api/v1/usuarios/<id>
        Resultado esperado: 200 OK con datos actualizados
        """
        # Crear un usuario de prueba
        usuario = UsuarioServiceTest.usuario_creation()
        usuario_creado = UsuarioService.create(usuario)

        # Actualizar el usuario
        usuario_actualizado = {
            "nombre": "Usuario Actualizado",
            "email": "actualizado@example.com",
            "password_hash": "newpassword456",
            "rol": "admin",
            "plan": "premium"
        }

        response = self.client.put(
            f'/api/v1/usuarios/{usuario_creado.id}',
            data=json.dumps(usuario_actualizado),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Usuario actualizado en el sistema")
        self.assertEqual(data['data']['nombre'], "Usuario Actualizado")
        self.assertEqual(data['data']['email'], "actualizado@example.com")

    def test_api_put_actualizar_usuario_no_existente(self):
        """
        Test API: Intentar actualizar un usuario que no existe.
        Endpoint: PUT /api/v1/usuarios/<id>
        Resultado esperado: 404 Not Found
        """
        usuario_data = {
            "nombre": "Usuario Fantasma",
            "email": "fantasma@example.com",
            "password_hash": "password123",
            "rol": "usuario",
            "plan": "básico"
        }

        response = self.client.put(
            '/api/v1/usuarios/9999',
            data=json.dumps(usuario_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "Usuario no encontrado")

    def test_repository_add_vs_merge(self):
        """
        Diferencia entre db.add() y db.merge() en el Repository
        
        - Repository.create() usa db.add(): Para objetos NUEVOS
        - Repository.update() usa db.merge(): Para ACTUALIZAR existentes
        
        Este test respeta la arquitectura Service -> Repository -> DB
        """
        from app.models import Usuario
        from app.repositories import UsuarioRepository
        
        # 1. CREATE con db.add() - Para objetos nuevos
        usuario_nuevo = Usuario(
            nombre="Usuario Nuevo",
            email="nuevo@test.com",
            password_hash="hash123",
            rol="usuario",
            plan="básico"
        )
        
        # Repository.create() usa db.add() internamente
        usuario_creado = UsuarioRepository.create(usuario_nuevo)
        
        self.assertIsNotNone(usuario_creado.id)
        self.assertEqual(usuario_creado.nombre, "Usuario Nuevo")
        
        # 2. UPDATE con db.merge() - Para objetos existentes
        usuario_existente = UsuarioRepository.get_by_id(usuario_creado.id)
        usuario_existente.nombre = "Usuario Actualizado"
        usuario_existente.rol = "admin"
        
        # Repository.update() usa db.merge() internamente
        usuario_actualizado = UsuarioRepository.update(usuario_existente)
        
        self.assertEqual(usuario_actualizado.nombre, "Usuario Actualizado")
        self.assertEqual(usuario_actualizado.rol, "admin")
        
        # Verificar que se actualizó correctamente
        usuario_verificado = UsuarioRepository.get_by_id(usuario_creado.id)
        self.assertEqual(usuario_verificado.nombre, "Usuario Actualizado")
        self.assertEqual(usuario_verificado.rol, "admin")
    

if __name__ == '__main__':
    unittest.main()

