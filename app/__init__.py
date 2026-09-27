import os
from flask import Flask
from app.database import init_db

def create_app(test_config=None):
    """
    Application factory for the Retail Order Management and Analytics Platform.
    """
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'retail-qe-secret-key-2026'),
        DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///retail_orders.db'),
        TESTING=False
    )

    if test_config:
        app.config.update(test_config)

    # Initialize database
    init_db(app)

    # Register blueprints
    from app.routes_api import api_bp
    from app.routes_web import web_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(web_bp, url_prefix='')

    return app
