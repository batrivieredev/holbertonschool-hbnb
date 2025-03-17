"""
Module gérant l'API des lieux.
Permet la gestion complète des locations et hébergements.

Fonctionnalités:
    - Création/modification de lieux
    - Association avec les équipements
    - Gestion des avis et notes
    - Recherche géolocalisée
"""

from flask_restx import Namespace, Resource, fields
from app.services.PlaceFacade import PlaceFacade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

facade = PlaceFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.doc(security='jwt')
    @jwt_required()  # Protection de la création
    @api.response(201, 'Place successfully created')
    @api.response(403, 'Unauthorized')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place (auth required)"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user['id']
        new_place = facade.create_place(place_data)

        if not new_place:
            return {'error': 'Failed to create place'}, 400

        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()  # Fetch places with owners correctly
            return places, 200
        except Exception as e:
            print(f"❌ Error retrieving places: {str(e)}")  # Debugging logs
            return {'error': 'An error occurred while retrieving places'}, 500




@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': place.owner.to_dict() if place.owner else None,  # ✅ Ensure owner is correctly formatted
            'amenities': [amenity.to_dict() for amenity in place.amenities] if place.amenities else [],  # ✅ Replace `add_amenity`
            'reviews': [review.to_dict() for review in place.reviews] if place.reviews else []  # ✅ Replace `add_review`
        }, 200

    @api.expect(place_model)
    @api.doc(security='jwt')
    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized - Not the owner')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place (Only the owner or admin can modify)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not current_user.get('is_admin') and str(place['owner']['id']) != str(current_user.get('id')):
            return {'error': 'Unauthorized action'}, 403

        updated_place = facade.update_place(place_id, request.json)

        if not updated_place:
            return {'error': 'Update failed'}, 400  # <- This might be triggering incorrectly

        # ✅ Fix: Always return a 200 response if the update succeeds
        return updated_place, 200