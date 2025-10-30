from flask import Blueprint, request
from app.validators.validators import validate_with
from app.mapping import ResponseSchema, ArticuloSchema
from app.service import ResponseBuilder
from app.service.calculadora_service import CalculadoraService, ArticuloDTO

calculadora_bp = Blueprint("calculadora", __name__)
message_mapper = ResponseSchema()

@calculadora_bp.route("/calcular", methods=["POST"])
@validate_with(ArticuloSchema)
def calcular():
    data = request.get_json(silent=True) or {}
    dto = ArticuloDTO(
        tipo_producto=data["tipo_producto"],
        categoria_peso=data["categoria_peso"],
        origen=data["origen"],
        valor_usd=data["valor_usd"],
        unidades=int(data["unidades"]),
        modo_precio=(data.get("modo_precio") or ("CIF" if data.get("es_cif") else "FOB")).upper()
    )

    result = CalculadoraService.calcular(dto)
    rb = ResponseBuilder()
    message = (
        rb.add_message("Cálculo generado")
          .add_status_code(200)
          .add_data(result)
          .add_path("/api/v1/calculadora/calcular")
          .build()
    )
    return message_mapper.dump(message, many=False), 200
