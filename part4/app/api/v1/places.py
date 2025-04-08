from flask import jsonify, request, Blueprint

# Create Places blueprint
places_bp = Blueprint('places', __name__)

from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

@places_bp.route('/places', methods=['GET'])
def get_places():
    """Get list of places with optional price filter."""
    try:
        max_price = request.args.get('max_price', type=float)
        places = Place.query

        if max_price is not None:
            places = places.filter(Place.price <= max_price)

        places = places.all()
        return jsonify([place.to_dict() for place in places]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>', methods=['GET'])
def get_place(place_id):
    """Get details of a specific place."""
    try:
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'error': 'Place not found'}), 404
        return jsonify(place.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    """Create a new place."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        place = Place.create_place(data, current_user_id)
        return jsonify(place.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    """Update a place."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Place not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        place.update_from_dict(data)
        return jsonify(place.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    """Delete a place."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Place not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        place.delete()
        return jsonify({'message': 'Place deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>/amenities', methods=['POST'])
@jwt_required()
def add_amenity_to_place(place_id):
    """Add an amenity to a place."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Place not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        from app.models.amenity import Amenity
        amenity = Amenity.query.get(data.get('amenity_id'))

        if not amenity:
            return jsonify({'error': 'Amenity not found'}), 404

        place.add_amenity(amenity)
        return jsonify(place.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
