from app.models import Usuario
from app import db
from typing import List

class UsuarioRepository: 

    @staticmethod
    def create(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def get_by_id(id: int) -> Usuario:

        return db.session.query(Usuario).filter_by(id=id).first()
    
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