from flask_restx import Namespace, Resource, fields
from app.services.PlaceFacade import PlaceFacade

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

facade = PlaceFacade()

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.String, description="List of reviews on the place")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        new_place = facade.create_place(place_data)
<<<<<<< HEAD
        if not new_place:
            return {'error': 'Failed to create place. Owner not found or duplicate title.'}, 400
=======

>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb
        return {
            'id': new_place.id,
            'title': new_place.title,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner': {
                'id': new_place.owner.id,
                'first_name': new_place.owner.first_name,
                'last_name': new_place.owner.last_name,
                'email': new_place.owner.email
<<<<<<< HEAD
            } if new_place.owner else None,  # Ajout de la vérification pour owner
            'amenity': new_place.add_amenity,
            'review': new_place.add_review
=======
            } if new_place.owner else None,
            'amenities': new_place.amenities,
            'reviews': new_place.reviews
>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
<<<<<<< HEAD
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



=======
        places = facade.get_all_places()
        print(f"🔍 Debug: Places retrieved: {places}")  # Ajout du debug
>>>>>>> 1ff6b64a9ea752b5780ce425352b4aa8d1d6d6cb

        formatted_places = []
        for place in places:
            if isinstance(place, dict):  # 🔥 Vérifie si c'est un dict
                print("⚠️ Warning: Found a dictionary instead of a Place object!", place)
                continue  # Ignore les dicts corrompus

            formatted_places.append({
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
                } if place.owner else None,
                'amenities': place.amenities,
                'reviews': place.reviews
            })

        return formatted_places, 200


@api.route('/<string:place_id>')
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
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            } if place.owner else None,
            'amenities': place.amenities,
            'reviews': place.reviews
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)

        if not updated_place:
            return {'error': 'Place not found'}, 404

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner': {
                'id': updated_place.owner.id,
                'first_name': updated_place.owner.first_name,
                'last_name': updated_place.owner.last_name,
                'email': updated_place.owner.email
            } if updated_place.owner else None,
            'amenities': updated_place.amenities,
            'reviews': updated_place.reviews
        }, 200
