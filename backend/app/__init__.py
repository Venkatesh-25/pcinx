"""
FRA Atlas DSS - Flask Application Factory
Production-ready Flask backend for Smart India Hackathon 2025
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.settings import Config
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.claims import claims_bp
    from app.routes.monitoring import monitoring_bp
    from app.routes.analytics import analytics_bp
    from app.routes.alerts import alerts_bp
    
    app.register_blueprint(claims_bp, url_prefix='/api/claims')
    app.register_blueprint(monitoring_bp, url_prefix='/api/monitoring')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'service': 'FRA Atlas DSS Backend',
            'version': '1.0.0'
        }
    
    @app.route('/')
    def index():
        return {
            'message': 'FRA Atlas DSS API',
            'documentation': '/docs',
            'health': '/health',
            'endpoints': {
                'claims': '/api/claims',
                'monitoring': '/api/monitoring',
                'analytics': '/api/analytics',
                'alerts': '/api/alerts'
            }
        }
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/fra_atlas.log', maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FRA Atlas DSS startup')
    
    return app

# Import models to ensure they're registered
from app.models import fra_claim, monitoring_data, alert