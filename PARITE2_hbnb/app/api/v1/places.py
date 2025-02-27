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

        title = place_data.get('title')
        if not title:
            return {'error': 'Title is required'}, 400

        price = place_data.get('price')
        if not price:
            return {'error': 'Price is required'}, 400
        if price is None or price <= 0:
            return {'error': 'Price must be a positive number'}, 400

        latitude = place_data.get('latitude')
        if not latitude:
            return {'error': 'Latitude is required'}, 400
        if latitude is None or latitude < -90 or latitude > 90:
            return {'error': 'Latitude must be a number between -90 and 90'}, 400

        longitude = place_data.get('longitude')
        if not longitude:
            return {'error': 'Longitude is required'}, 400
        if longitude is None or longitude < -180 or longitude > 180:
            return {'error': 'Longitude must be a number between -180 and 180'}, 400

        owner_id = place_data.get('owner_id')
        if not owner_id:
            return {'error': 'Owner ID is required'}, 400

        amenities = place_data.get('amenities')
        if not amenities:
            return {'error': 'Amenities are required'}, 400

        new_place = facade.create_place(place_data)

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
            } if new_place.owner else None,
            'amenities': new_place.amenities,
            'reviews': new_place.reviews
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        print(f"🔍 Debug: Places retrieved: {places}")  # Ajout du debug

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
