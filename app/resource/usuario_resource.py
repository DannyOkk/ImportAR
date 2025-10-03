from flask import Blueprint, jsonify
from app.mapping import UsuarioSchema, ResponseSchema
from app.service import UsuarioService, ResponseBuilder
from app.models.usuario import Usuario


usuario_bp = Blueprint('usuario', __name__)
usuario_mapper = UsuarioSchema()
message_mapper = ResponseSchema()

@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    usuarios= UsuarioService.read_all()
    return usuario_mapper.dump(usuarios,many=True), 200

@usuario_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id: int):
    usuario = UsuarioService.get_by_id(id)
    rb= ResponseBuilder()
    if not usuario:
        message=rb.add_message("Usuario no encontrado").add_status_code(404).add_data({}).add_path(f"/api/v1/usuarios/{id}").build()
        
        return message_mapper.dump(message, many=False), 404
    message=rb.add_message("Usuario encontrado").add_status_code(100).add_data(usuario_mapper.dump(usuario)).add_path(f"/api/v1/usuarios/{id}").build()
    return message_mapper.dump(message, many=False), 200
