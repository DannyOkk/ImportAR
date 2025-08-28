from app.models import Usuario
from app.repositories import UsuarioRepository
from typing import List

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
    def get_by_id(id: int) -> Usuario:
        """
        Retrieve a user by their ID.
        :param id: The ID of the user to retrieve.
        :return: The Usuario object if found, else None.
        """
        return UsuarioRepository.get_by_id(id)

    @staticmethod   
    def read_all() -> list[Usuario]:
        """
        Retrieve all users from the database.
        :return: A list of all Usuario objects.
        """
        return UsuarioRepository.read_all()

