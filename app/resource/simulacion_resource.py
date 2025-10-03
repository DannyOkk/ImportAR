from app.validators.validators import validate_with
from flask import Blueprint, jsonify, request
from app.mapping import ResponseSchema
from app.service import ResponseBuilder, SimulacionService
from app.models import Simulacion


simulacion_bp = Blueprint('simulacion', __name__)
message_mapper = ResponseSchema()

@simulacion_bp.route('/generar', methods=['GET'])
def generar_simulacion():
    simulacion = Simulacion()

    result= SimulacionService.execute(simulacion)
    rb= ResponseBuilder()
    message=rb.add_message("Simulación generada").add_status_code(201).add_data({'resultado':result}).add_path(f"/api/v1/simulaciones/generar").build()
        
    return message_mapper.dump(message, many=False), 201