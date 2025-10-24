from flask import Blueprint, request
from http import HTTPStatus

from app.mapping import ResponseSchema
from app.service import ResponseBuilder, SimulacionService
from app.models import Simulacion
from app.repositories import SimulacionRepository

simulacion_bp = Blueprint('simulacion', __name__)
message_mapper = ResponseSchema()

# Función para detectar el "usuario autenticado"
def _resolve_usuario_id():
    # 1) Header: X-User-Id
    hdr = request.headers.get('X-User-Id')
    if hdr and hdr.isdigit():
        return int(hdr)
    # 2) Body JSON: usuario_id
    body = request.get_json(silent=True) or {}
    uid = body.get("usuario_id")
    if uid and str(uid).isdigit():
        return int(uid)
    return None


#Crear simulación asociada al usuario
@simulacion_bp.route('/generar', methods=['POST'])
def generar_simulacion():
    usuario_id = _resolve_usuario_id()

    if not usuario_id:
        rb = ResponseBuilder()
        message = (rb.add_message("Falta X-User-Id en headers o usuario_id en el body")
                     .add_status_code(HTTPStatus.BAD_REQUEST)
                     .add_path("/api/v1/simulaciones/generar")
                     .build())
        return message_mapper.dump(message, many=False), HTTPStatus.BAD_REQUEST

    # Creamos DTO con usuario asignado
    dto = Simulacion()
    dto.usuario_id = usuario_id

    result = SimulacionService.execute(dto)

    rb = ResponseBuilder()
    status = HTTPStatus.CREATED if result else HTTPStatus.BAD_REQUEST
    message = (rb.add_message("Simulación generada" if result else "No se pudo ejecutar la simulación")
                 .add_status_code(status)
                 .add_data({'resultado': result})
                 .add_path("/api/v1/simulaciones/generar")
                 .build())

    return message_mapper.dump(message, many=False), status


#Listar solo simulaciones del usuario autenticado
@simulacion_bp.route('', methods=['GET'])
def listar_simulaciones():
    usuario_id = _resolve_usuario_id()

    if not usuario_id:
        rb = ResponseBuilder()
        message = (rb.add_message("Falta X-User-Id en headers o usuario_id en el body")
                     .add_status_code(HTTPStatus.BAD_REQUEST)
                     .add_path("/api/v1/simulaciones")
                     .build())
        return message_mapper.dump(message, many=False), HTTPStatus.BAD_REQUEST

    simulaciones = SimulacionRepository.read_by_usuario(usuario_id)

    data = [{
        'id': s.id,
        'usuario_id': s.usuario_id,
        'estado': s.estado,
        'num_escenario': s.num_escenario,
        'presupuesto_id': s.presupuesto_id,
        'fecha_creacion': s.fecha_creacion.isoformat() if s.fecha_creacion else None,
        'fecha_finalizacion': s.fecha_finalizacion.isoformat() if s.fecha_finalizacion else None
    } for s in simulaciones]

    rb = ResponseBuilder()
    message = (rb.add_message("Listado de simulaciones del usuario")
                 .add_status_code(HTTPStatus.OK)
                 .add_data({'items': data, 'count': len(data)})
                 .add_path("/api/v1/simulaciones")
                 .build())
    return message_mapper.dump(message, many=False), HTTPStatus.OK
