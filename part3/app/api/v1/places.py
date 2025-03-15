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

facade = PlaceFacade()

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Titre de l\'annonce', example="Appartement centre-ville"),
    'description': fields.String(description='Description détaillée'),
    'price': fields.Float(required=True, description='Prix par nuit', example=100.0),
    'latitude': fields.Float(required=True, description='Latitude GPS', example=48.8566),
    'longitude': fields.Float(required=True, description='Longitude GPS', example=2.3522),
    'owner_id': fields.String(required=True, description='ID du propriétaire'),
    'amenities': fields.List(fields.String, description='Liste des IDs des équipements')
})

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
        places = facade.get_all_places()  # Récupère tous les lieux

        # Retourne une liste formatée avec les détails des lieux
        return [{
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            } if place.owner else None,  # Vérifie si le propriétaire existe
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities] if place.amenities else [],  # Assure-toi que amenities est une liste
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            } for review in place.reviews] if place.reviews else []  # Pareil pour les reviews
        } for place in places], 200




@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.title, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner': place.owner, 'amenity': place.add_amenity, 'review': place.add_review}, 200

    @api.expect(place_model)
    @api.doc(security='jwt')
    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized - Not the owner')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place (owner only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        # Les admins peuvent modifier n'importe quel lieu
        if not current_user.get('is_admin'):
            if str(place.owner_id) != str(current_user.get('id')):
                return {'error': 'Not authorized'}, 403

        place_data = api.payload
        place = facade.update_place(place_id, place_data)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.title, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude, 'owner': place.owner, 'amenity': place.add_amenity, 'review': place.add_review}, 200

# Adding the review model
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
