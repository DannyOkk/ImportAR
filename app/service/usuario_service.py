from app.models import Usuario
from app.repositories import UsuarioRepository
from typing import List
from app.service import EncrypterService, EncrypterManager, StandardEncrypterService, PasslibEncrypterService

class UsuarioService:
    @staticmethod
    def create(usuario:Usuario)-> Usuario: 
        """
        Create a new user in the database.
        :param usuario: Usuario object to be created.   
        :return: The created Usuario object.
        """
        usuario.password_hash = EncrypterManager.hash_password(usuario.password_hash)
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

    @staticmethod
    def update(usuario: Usuario, id: int) -> Usuario:
        """
        Update an existing user in the database.
        :param usuario: Usuario object with updated data.
        :param id: The ID of the user to update.
        :return: The updated Usuario object.
        """
        existing_usuario = UsuarioService.get_by_id(id)
        if not existing_usuario:
            return None
        #TODO: Si el password ha cambiado, encriptarlo de nuevo, sino dejarlo igual
        existing_usuario.nombre = usuario.nombre
        existing_usuario.email = usuario.email
        existing_usuario.password_hash = usuario.password_hash
        existing_usuario.rol = usuario.rol
        existing_usuario.plan = usuario.plan

        UsuarioRepository.update(existing_usuario)

        return existing_usuario

    @staticmethod
    def delete(id: int) -> bool:
        """
        Delete a user from the database.
        :param id: The ID of the user to delete.
        :return: True if deletion was successful, else False.
        """
        usuario = UsuarioService.get_by_id(id)
        if not usuario:
            return False
        
        UsuarioRepository.delete(usuario)
        return True
