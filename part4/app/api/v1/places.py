from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.extensions import db
import traceback

places_bp = Blueprint('places', __name__)

@places_bp.route('/places', methods=['GET'])
def get_places():
    try:
        max_price = request.args.get('max_price', type=float)
        query = Place.query
        if max_price is not None:
            query = query.filter(Place.price <= max_price)
        places = query.all()
        return jsonify([place.to_dict() for place in places]), 200
    except Exception as e:
        print(f"Error fetching places: {str(e)}")
        return jsonify({'message': 'Error fetching places'}), 500

@places_bp.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    try:
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'message': 'Place not found'}), 404
        return jsonify(place.to_dict()), 200
    except Exception as e:
        print(f"Error fetching place: {str(e)}")
        return jsonify({'message': 'Error fetching place'}), 500

@places_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    try:
        # Get and verify user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"message": "User not found"}), 401

        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        required_fields = ['title', 'description', 'price', 'latitude', 'longitude']
        if not all(k in data for k in required_fields):
            missing_fields = [k for k in required_fields if k not in data]
            return jsonify({
                'message': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400

        try:
            price = float(data['price'])
            if price <= 0:
                return jsonify({'message': 'Price must be greater than 0'}), 400

            latitude = float(str(data['latitude']).replace(',', '.'))
            longitude = float(str(data['longitude']).replace(',', '.'))

            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                return jsonify({'message': 'Invalid latitude or longitude values'}), 400

        except ValueError as ve:
            print(f"Value error parsing numbers: {str(ve)}")
            return jsonify({'message': 'Invalid number format for price, latitude, or longitude'}), 400

        # Create place
        place = Place(
            title=data['title'].strip(),
            description=data['description'].strip(),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=current_user_id
        )

        try:
            db.session.add(place)
            db.session.commit()
            return jsonify(place.to_dict()), 201
        except Exception as db_error:
            db.session.rollback()
            print(f"Database error creating place: {str(db_error)}")
            print(traceback.format_exc())
            return jsonify({'message': 'Database error while creating place'}), 500

    except Exception as e:
        print(f"General error in create_place: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'message': 'An error occurred while creating the place'}), 500

@places_bp.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    try:
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'message': 'Place not found'}), 404

        reviews = Review.query.filter_by(place_id=place_id).all()
        return jsonify([review.to_dict() for review in reviews]), 200
    except Exception as e:
        print(f"Error fetching reviews: {str(e)}")
        return jsonify({'message': 'Error fetching reviews'}), 500

@places_bp.route('/places/<place_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(place_id):
    try:
        # Get and verify user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 401

        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        if 'text' not in data or 'rating' not in data:
            return jsonify({'message': 'Missing text or rating'}), 400

        try:
            rating = int(data['rating'])
            if not (1 <= rating <= 5):
                return jsonify({'message': 'Rating must be between 1 and 5'}), 400
        except ValueError:
            return jsonify({'message': 'Rating must be a number'}), 400

        # Check if place exists
        place = Place.query.get(place_id)
        if not place:
            return jsonify({'message': 'Place not found'}), 404

        # Check for existing review
        if Review.query.filter_by(place_id=place_id, user_id=current_user_id).first():
            return jsonify({'message': 'You have already reviewed this place'}), 400

        # Create review
        review = Review(
            text=data['text'].strip(),
            rating=rating,
            place_id=place_id,
            user_id=current_user_id
        )

        try:
            db.session.add(review)
            db.session.commit()
            return jsonify(review.to_dict()), 201
        except Exception as db_error:
            db.session.rollback()
            print(f"Database error creating review: {str(db_error)}")
            print(traceback.format_exc())
            return jsonify({'message': 'Database error while creating review'}), 500

    except Exception as e:
        print(f"General error in create_review: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'message': 'An error occurred while creating the review'}), 500
