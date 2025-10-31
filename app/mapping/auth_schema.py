from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """Schema para validar credenciales de login."""
    email = fields.Email(required=True, error_messages={
        "required": "El email es requerido",
        "invalid": "El email no tiene un formato válido"
    })
    password = fields.Str(required=True, validate=validate.Length(min=1), error_messages={
        "required": "La contraseña es requerida"
    })


class RegisterSchema(Schema):
    """Schema para validar registro de nuevo usuario."""
    nombre = fields.Str(required=True, validate=validate.Length(min=2), error_messages={
        "required": "El nombre es requerido"
    })
    email = fields.Email(required=True, error_messages={
        "required": "El email es requerido",
        "invalid": "El email no tiene un formato válido"
    })
    password = fields.Str(required=True, validate=validate.Length(min=6), error_messages={
        "required": "La contraseña es requerida",
        "invalid": "La contraseña debe tener al menos 6 caracteres"
    })
    rol = fields.Str(load_default="usuario")
    plan = fields.Str(load_default="básico")
