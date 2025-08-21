import datetime

from app.models import Usuario

class UsuarioServiceTest:
    
    @staticmethod
    def usuario_creation() -> Usuario: 
        usuario = Usuario()
        usuario.nombre = "Test User"
        usuario.email = "test@example.com"
        usuario.password = "securepassword"
        usuario.rol = "admin"
        usuario.plan = "basic"
        usuario.fecha_alta = datetime.datetime.now()
        return usuario