from app.models import Usuario
from app.repositories import UsuarioRepository
from app.service import EncrypterManager

class AuthService:
    """
    Service para manejar autenticación de usuarios.
    Sigue el patrón KISS y CRUD del proyecto.
    """
    
    @staticmethod
    def login(email: str, password: str) -> Usuario:
        """
        Autentica un usuario con email y contraseña.
        
        :param email: Email del usuario.
        :param password: Contraseña en texto plano.
        :return: Usuario autenticado si las credenciales son correctas.
        :raises ValueError: Si las credenciales son inválidas.
        """
        # Buscar usuario por email
        usuario = UsuarioRepository.get_by_email(email)
        
        if not usuario:
            raise ValueError("Credenciales inválidas")
        
        # Verificar contraseña
        if not EncrypterManager.check_password(usuario.password_hash, password):
            raise ValueError("Credenciales inválidas")
        
        return usuario
    
    @staticmethod
    def register(nombre: str, email: str, password: str, rol: str = "usuario", plan: str = "básico") -> Usuario:
        """
        Registra un nuevo usuario en el sistema.
        
        :param nombre: Nombre del usuario.
        :param email: Email del usuario.
        :param password: Contraseña en texto plano.
        :param rol: Rol del usuario (default: "usuario").
        :param plan: Plan del usuario (default: "básico").
        :return: Usuario registrado.
        :raises ValueError: Si el email ya está registrado.
        """
        # Verificar si el email ya existe
        existing_usuario = UsuarioRepository.get_by_email(email)
        if existing_usuario:
            raise ValueError(f"El email {email} ya está registrado en el sistema")
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=EncrypterManager.hash_password(password),
            rol=rol,
            plan=plan
        )
        
        # Guardar en la base de datos
        UsuarioRepository.create(nuevo_usuario)
        
        return nuevo_usuario
