from marshmallow import Schema, fields, validates_schema, ValidationError, validate
import re
import unicodedata

# Opciones rápidas (catálogo embebido en el schema)
TIPOS = ["celulares", "notebooks"]
CATEGORIAS = {
    "celulares": ["Ultra livianos", "Livianos estándar", "Peso medio", "Pesados/Potentes", "Muy pesados/Superphones"],
    "notebooks": ["Ultrabook", "Convertible", "Estandar/Productividad", "Gaming ligero", "Gaming/Alto rendimiento", "Workstation/Profesional"],
}

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
        # Ignora campos desconocidos para no fallar si vienen extras
        unknown = 'exclude'

    tipo_producto = fields.Str(required=True)
    categoria_peso = fields.Str(required=True)
    origen = fields.Str(required=True)
    valor_usd = fields.Float(required=True)
    unidades = fields.Int(required=True)
    # Opcionales para el flujo: uno u otro
    modo_precio = fields.Str(required=False, validate=validate.OneOf(["CIF", "FOB"]))
    es_cif = fields.Boolean(required=False)

    @validates_schema
    def validar_dependencias(self, data, **kwargs):
        def _norm(s: str) -> str:
            s = (s or "").strip()
            # Normaliza acentos
            s = unicodedata.normalize('NFKD', s)
            s = ''.join(ch for ch in s if not unicodedata.combining(ch))
            # Unifica separadores a espacios
            s = re.sub(r"[/\\\-]+", " ", s)
            # Colapsa cualquier whitespace (incl. NBSP) a un solo espacio
            s = ' '.join(s.split())
            s = s.lower()
            return s

        tipo = _norm(data.get("tipo_producto"))
        cat = _norm(data.get("categoria_peso"))
        origen = (data.get("origen") or "").strip().upper()
        valor = data.get("valor_usd", -1)
        unidades = data.get("unidades", 0)

        # tipo
        if tipo not in TIPOS:
            raise ValidationError({
                "tipo_producto": [f"Debe ser uno de: {', '.join(TIPOS)}"]
            })
        # categoria dependiente de tipo
        categorias_validas = CATEGORIAS.get(tipo, [])
        categorias_validas_map = {}
        for c in categorias_validas:
            categorias_validas_map[_norm(c)] = c
        if cat not in categorias_validas_map:
            raise ValidationError({
                "categoria_peso": [f"Para tipo '{tipo}', use: {', '.join(categorias_validas)}"]
            })
        # origen (acepta US/CN)
        if origen not in ("US", "CN"):
            raise ValidationError({
                "origen": ["Debe ser 'US' o 'CN'"]
            })
        # valores numéricos
        if valor < 0:
            raise ValidationError({
                "valor_usd": ["Debe ser >= 0"]
            })
        if unidades < 1:
            raise ValidationError({
                "unidades": ["Debe ser >= 1"]
            })
