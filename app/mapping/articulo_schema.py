from marshmallow import Schema, fields, validates_schema, ValidationError, validate, post_load
import re
import unicodedata
from decimal import Decimal
from app.config.domain_constants import TIPOS, CATEGORIAS
from app.models.articulo import Articulo

class ArticuloSchema(Schema):
    """
    Valida artículo para la calculadora.
    - tipo_producto: debe ser uno de TIPOS
    - categoria_peso: depende del tipo_producto (CATEGORIAS[tipo])
    - origen: "US" | "CN"
    - valor_usd: >= 0 (CIF o FOB según flujo de negocio)
    - unidades: >= 1
    """
    class Meta:
        unknown = 'exclude'

    tipo_producto = fields.Str(required=True)
    categoria_peso = fields.Str(required=True)
    origen = fields.Str(required=True)
    valor_usd = fields.Float(required=True)
    unidades = fields.Int(required=True)
    modo_precio = fields.Str(
        required=True, validate=validate.OneOf(["CIF", "FOB"])
        )
    es_courier = fields.Boolean(required=False)

    @validates_schema
    def validar_dependencias(self, data, **kwargs):
        def _norm(s: str) -> str:
            s = (s or "").strip()
            s = unicodedata.normalize('NFKD', s)
            s = ''.join(ch for ch in s if not unicodedata.combining(ch))
            s = re.sub(r"[/\\\-]+", " ", s)
            s = ' '.join(s.split())
            s = s.lower()
            return s

        tipo = _norm(data.get("tipo_producto"))
        cat = _norm(data.get("categoria_peso"))
        origen = (data.get("origen") or "").strip().upper()
        valor = data.get("valor_usd", -1)
        unidades = data.get("unidades", 0)

        if tipo not in TIPOS:
            raise ValidationError({
                "tipo_producto": [f"Debe ser uno de: {', '.join(TIPOS)}"]
            })
        categorias_validas = CATEGORIAS.get(tipo, [])
        categorias_validas_map = {}
        for c in categorias_validas:
            categorias_validas_map[_norm(c)] = c
        if cat not in categorias_validas_map:
            raise ValidationError({
                "categoria_peso": [f"Para tipo '{tipo}', use: {', '.join(categorias_validas)}"]
            })
        if origen not in ("US", "CN"):
            raise ValidationError({
                "origen": ["Debe ser 'US' o 'CN'"]
            })
        if valor < 0:
            raise ValidationError({
                "valor_usd": ["Debe ser >= 0"]
            })
        if unidades < 1:
            raise ValidationError({
                "unidades": ["Debe ser >= 1"]
            })

    @post_load
    def make_articulo(self, data, **kwargs):
        """Convierte el dict validado a instancia de Articulo."""
        return Articulo(
            tipo_producto=data["tipo_producto"].lower(),
            categoria_peso=data["categoria_peso"].lower(),
            origen=data["origen"].upper(),
            valor_usd=Decimal(str(data["valor_usd"])),
            unidades=int(data["unidades"]),
            modo_precio=(data.get("modo_precio") or "FOB").upper(),
            es_courier=data.get("es_courier", False)
        )
