from flask_restx import Namespace, Resource, fields
from app.services.AmenityFacade import AmenityFacade


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = AmenityFacade()


@api.route('/')
class AmenityList(Resource):

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()

        # Si aucune amenity, renvoie une liste vide avec un status 200
        return ([] if not amenities else [{'id': amenity.id, 'name': amenity.name} for amenity in amenities]), 200

    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        name = amenity_data.get('name')

        # Vérification avant toute tentative de création
        if not name or not isinstance(name, str) or name.strip() == "":
            return {'error': 'Name is required and must be a non-empty string'}, 400

        existing_amenity = facade.get_amenity_by_name(name)
        if existing_amenity:
            return {'error': 'Name already registered'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        if not amenity_data or 'name' not in amenity_data or not amenity_data['name'].strip():
            return {'error': 'Invalid input data. Name is required and must be non-empty.'}, 400

        amenity = facade.update_amenity(amenity_id, amenity_data)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'id': amenity.id, 'name': amenity.name}, 200
