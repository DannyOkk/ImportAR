from flask import Blueprint, jsonify, request
from app.validators.validators import validate_with
from app.mapping import LoginSchema, RegisterSchema, UsuarioSchema, ResponseSchema
from app.service import AuthService, ResponseBuilder

auth_bp = Blueprint('auth', __name__)
login_schema = LoginSchema()
register_schema = RegisterSchema()
usuario_schema = UsuarioSchema()
response_schema = ResponseSchema()


@auth_bp.route('/login', methods=['POST'])
@validate_with(LoginSchema)
def login():
    """
    Endpoint para login de usuario.
    POST /api/v1/auth/login
    Body: { "email": "user@example.com", "password": "password123" }
    """
    data = login_schema.load(request.json)
    rb = ResponseBuilder()
    
    try:
        # Autenticar usuario
        usuario = AuthService.login(data['email'], data['password'])
        
        # Retornar datos del usuario (sin password)
        usuario_data = usuario_schema.dump(usuario)
        
        message = rb.add_message("Login exitoso").add_status_code(200).add_data({
            "usuario": usuario_data,
            "message": "Bienvenido al sistema"
        }).add_path("/api/v1/auth/login").build()
        
        return response_schema.dump(message), 200
        
    except ValueError as e:
        # Credenciales inválidas
        message = rb.add_message(str(e)).add_status_code(401).add_data({}).add_path("/api/v1/auth/login").build()
        return response_schema.dump(message), 401
        
    except Exception as e:
        # Error inesperado
        message = rb.add_message(f"Error en el servidor: {str(e)}").add_status_code(500).add_data({}).add_path("/api/v1/auth/login").build()
        return response_schema.dump(message), 500


@auth_bp.route('/register', methods=['POST'])
@validate_with(RegisterSchema)
def register():
    """
    Endpoint para registrar un nuevo usuario.
    POST /api/v1/auth/register
    Body: { "nombre": "Juan", "email": "juan@example.com", "password": "password123" }
    """
    data = register_schema.load(request.json)
    rb = ResponseBuilder()
    
    try:
        # Registrar usuario
        usuario = AuthService.register(
            nombre=data['nombre'],
            email=data['email'],
            password=data['password'],
            rol=data.get('rol', 'usuario'),
            plan=data.get('plan', 'básico')
        )
        
        # Retornar datos del usuario (sin password)
        usuario_data = usuario_schema.dump(usuario)
        
        message = rb.add_message("Usuario registrado exitosamente").add_status_code(201).add_data({
            "usuario": usuario_data
        }).add_path("/api/v1/auth/register").build()
        
        return response_schema.dump(message), 201
        
    except ValueError as e:
        # Email duplicado u otro error de validación
        message = rb.add_message(str(e)).add_status_code(409).add_data({}).add_path("/api/v1/auth/register").build()
        return response_schema.dump(message), 409
        
    except Exception as e:
        # Error inesperado
        message = rb.add_message(f"Error al registrar usuario: {str(e)}").add_status_code(500).add_data({}).add_path("/api/v1/auth/register").build()
        return response_schema.dump(message), 500
