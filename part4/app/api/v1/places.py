from flask import jsonify, request, Blueprint

# Create Places blueprint
places_bp = Blueprint('places', __name__)

from app.models.place import Place
from app.models.user import User
from app.models.place_photo import PlacePhoto
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

@places_bp.route('/places/<string:place_id>/photos', methods=['POST'])
@jwt_required()
def add_photo_to_place(place_id):
    """Add a photo to a place."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Place not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Create new photo
        photo = PlacePhoto(
            place_id=place_id,
            photo_url=data['photo_url'],
            caption=data.get('caption'),
            is_primary=data.get('is_primary', False)
        )

        # If this is the first photo or marked as primary, make sure it's the only primary
        if photo.is_primary:
            for existing_photo in place.photos:
                existing_photo.is_primary = False
        elif not place.photos:  # First photo is automatically primary
            photo.is_primary = True

        place.photos.append(photo)
        place.save()

        return jsonify(photo.to_dict()), 201
    except KeyError:
        return jsonify({'error': 'Missing required field: photo_url'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>/photos/<string:photo_id>', methods=['PUT'])
@jwt_required()
def update_place_photo(place_id, photo_id):
    """Update a place photo."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)
        photo = PlacePhoto.query.get(photo_id)

        if not place or not photo or photo.place_id != place_id:
            return jsonify({'error': 'Photo not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        if 'photo_url' in data:
            photo.photo_url = data['photo_url']
        if 'caption' in data:
            photo.caption = data['caption']
        if 'is_primary' in data and data['is_primary']:
            # Update other photos to non-primary
            for other_photo in place.photos:
                other_photo.is_primary = False
            photo.is_primary = True

        photo.save()
        return jsonify(photo.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@places_bp.route('/places/<string:place_id>/photos/<string:photo_id>', methods=['DELETE'])
@jwt_required()
def delete_place_photo(place_id, photo_id):
    """Delete a place photo."""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)
        photo = PlacePhoto.query.get(photo_id)

        if not place or not photo or photo.place_id != place_id:
            return jsonify({'error': 'Photo not found'}), 404

        if place.owner_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        was_primary = photo.is_primary
        photo.delete()

        # If we deleted the primary photo, make another one primary
        if was_primary and place.photos:
            place.photos[0].is_primary = True
            place.photos[0].save()

        return jsonify({'message': 'Photo deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
