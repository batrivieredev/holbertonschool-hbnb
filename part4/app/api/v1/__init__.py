from flask import Blueprint
from .users import users_bp
from .auth import auth_bp
from .places import places_bp

api_v1 = Blueprint('api_v1', __name__)

# Register all blueprints
api_v1.register_blueprint(users_bp)
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(places_bp)
