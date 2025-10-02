from marshmallow import Schema, fields, post_load
from app.models import Usuario

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Str(load_only=True, required=True)
    rol = fields.Str(required=True)
    plan = fields.Str(required=True)
    fecha_alta = fields.DateTime(dump_only=True)

    @post_load
    def make_usuario(self, data, **kwargs):
        return Usuario(**data)