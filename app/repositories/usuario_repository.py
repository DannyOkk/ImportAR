from app.models import Usuario
from app import db
class UsuarioRepository: 

    @staticmethod
    def create(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    