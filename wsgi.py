"""
WSGI entry point for Gunicorn
"""
from app import create_app
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Create the Flask application
application = create_app()
app = application

# Push app context
app.app_context().push()
