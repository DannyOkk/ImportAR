from app.validators.validators import validate_with
from flask import Blueprint, jsonify, request
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


@usuario_bp.route('/', methods=['POST'])
@validate_with(UsuarioSchema)
def create_usuario():
    usuario = usuario_mapper.load(request.json)
    UsuarioService.create(usuario)
    rb= ResponseBuilder()
    message=rb.add_message("Usuario creado en el sistema").add_status_code(201).add_data({}).add_path(f"/api/v1/usuarios/").build()
        
    return message_mapper.dump(message, many=False), 201

@usuario_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id: int):
    usuario_data = usuario_mapper.load(request.json)
    usuario = UsuarioService.update(usuario_data, id)
    rb= ResponseBuilder()
    if not usuario:
        message=rb.add_message("Usuario no encontrado").add_status_code(404).add_data({}).add_path(f"/api/v1/usuarios/{id}").build()
        
        return message_mapper.dump(message, many=False), 404
    message=rb.add_message("Usuario actualizado en el sistema").add_status_code(200).add_data(usuario_mapper.dump(usuario)).add_path(f"/api/v1/usuarios/{id}").build()
        
    return message_mapper.dump(message, many=False), 200

 
