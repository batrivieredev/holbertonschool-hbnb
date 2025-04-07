from flask import Flask, send_from_directory
from flask_cors import CORS
from app.extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object('config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API blueprint
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Serve static files
    @app.route('/')
    def serve_index():
        return send_from_directory('../static', 'index.html')

    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('../static', path)

    @app.route('/<path:path>.html')
    def serve_html(path):
        return send_from_directory('../static', f'{path}.html')

    return app
