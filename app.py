import os
from flask import Flask
from models import db
from routes.dashboard import dashboard_bp
from routes.aircraft import aircraft_bp
from routes.analytics import analytics_bp
from routes.airport import airport_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///aeroscope.db'
    ).replace('postgres://', 'postgresql://')  # Render fix
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(aircraft_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)),
            debug=app.config['DEBUG'])
