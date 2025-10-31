from flask import Blueprint, request
from app.validators.validators import validate_with
from app.mapping import ResponseSchema, ArticuloSchema
from app.service import ResponseBuilder
from app.service.presupuesto_service import PresupuestoService

presupuesto_bp = Blueprint("presupuesto", __name__)
message_mapper = ResponseSchema()

@presupuesto_bp.route("/calcular", methods=["POST"])
@validate_with(ArticuloSchema)
def calcular():
    data = request.get_json(silent=True) or {}
    articulo = ArticuloSchema().load(data)  

    result = PresupuestoService.calcular(articulo)
    rb = ResponseBuilder()
    message = (
        rb.add_message("Cálculo generado")
          .add_status_code(200)
          .add_data(result)
          .add_path("/api/v1/presupuesto/calcular")
          .build()
    )
    return message_mapper.dump(message, many=False), 200
