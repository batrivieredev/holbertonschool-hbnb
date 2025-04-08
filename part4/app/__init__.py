from flask import Flask, send_from_directory
from flask_cors import CORS
from app.extensions import db, bcrypt, jwt
import os

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Authorization"],
        "supports_credentials": True
    }})

    # Register API blueprint
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Serve static files
    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def serve_static(path):
        if path.endswith('.js'):
            return send_from_directory(os.path.join(app.static_folder, 'js'), path)
        elif path.endswith('.css'):
            return send_from_directory(os.path.join(app.static_folder, 'css'), path)
        elif path.endswith('.html'):
            return send_from_directory(app.static_folder, path)
        elif path.endswith('.html'):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app
