from flask import Blueprint, jsonify

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