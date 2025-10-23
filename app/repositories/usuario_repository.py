from app.models import Usuario
from app import db
from typing import List
from app.repositories import Create, Read, Update, Delete

class UsuarioRepository(Create, Read, Update, Delete): 

    @staticmethod
    def create(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def get_by_id(id: int) -> Usuario:

        return db.session.query(Usuario).filter_by(id=id).first()
    
    @staticmethod
    def get_by_email(email: str) -> Usuario:
        """
        Retrieve a user by their email address.
        :param email: The email of the user to retrieve.
        :return: The Usuario object if found, else None.
        """
        return db.session.query(Usuario).filter_by(email=email).first()
    
    @staticmethod
    def read_all() -> list[Usuario]:
        return db.session.query(Usuario).all()
    
    @staticmethod
    def update(usuario: Usuario) -> Usuario:
        db.session.merge(usuario)
        db.session.commit()
        return usuario
    
    @staticmethod
    def delete(usuario: Usuario) -> None:
        db.session.delete(usuario)
        db.session.commit()