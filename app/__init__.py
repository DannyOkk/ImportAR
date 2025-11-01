import logging
from flask import Flask
import os
from app.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app_context = os.getenv('FLASK_CONTEXT')
    #https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    # Habilitar CORS para todas las rutas
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000",      # React dev local
                "http://127.0.0.1:3000",     # React dev local
                "http://localhost",           # Frontend en Docker (puerto 80)
                "http://localhost:80",        # Frontend en Docker explícito
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from app.resource import home_bp, usuario_bp, presupuesto_bp, auth_bp
    app.register_blueprint(presupuesto_bp, url_prefix='/api/v1/presupuestos')
    app.register_blueprint(usuario_bp, url_prefix='/api/v1/usuarios')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(home_bp, url_prefix='/api/v1')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app


