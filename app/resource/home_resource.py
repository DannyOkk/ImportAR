from flask import Blueprint, jsonify
from app.service.apidolar_service import DolarApiService

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a ImportAR", "status": "ok"}), 200

@home_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "ImportAR API",
        "version": "1.0"
    }), 200

@home_bp.route('/cotizaciones', methods=['GET'])
def cotizaciones():
    tc_oficial, oficial_fallback = DolarApiService.get_a3500()
    
    tc_mep, mep_fallback = DolarApiService.get_mep()
    
    return jsonify({
        "oficial": {
            "valor": float(tc_oficial),
            "fue_fallback": oficial_fallback
        },
        "mep": {
            "valor": float(tc_mep),
            "fue_fallback": mep_fallback
        }
    }), 200