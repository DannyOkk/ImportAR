from app.models import Usuario
from app.repositories import UsuarioRepository

class UsuarioService:
    @staticmethod
    def create(usuario:Usuario)-> Usuario: 
        """
        Create a new user in the database.
        :param usuario: Usuario object to be created.   
        :return: The created Usuario object.
        """
        UsuarioRepository.create(usuario)

        return usuario



