"""
Module gérant l'API des avis.
Implémente les endpoints REST pour la gestion des avis utilisateurs.

Fonctionnalités:
    - Création/modification/suppression d'avis
    - Notation des lieux (1-5 étoiles)
    - Filtrage par lieu/utilisateur
    - Pagination des résultats
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ReviewFacade import ReviewFacade
from app.services.PlaceFacade import PlaceFacade

api = Namespace('reviews', description='Review operations')

# Instance de la Facade
review_facade = ReviewFacade()
place_facade = PlaceFacade()

# Modèle de validation des données pour Swagger
review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description="Contenu de l'avis",
        example="Excellent séjour, très bon accueil"
    ),
    'rating': fields.Integer(
        required=True,
        description="Note sur 5",
        min=1,
        max=5,
        example=4
    ),
    'place_id': fields.String(required=True, description="ID du lieu concerné")
})


@api.route('/')
class ReviewList(Resource):
    @api.doc(security='jwt')
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized')
    def post(self):
        """Créer un nouvel avis"""
        current_user = get_jwt_identity()
        review_data = api.payload

        # Validation des entrées
        if not review_data.get('text') or not isinstance(review_data['text'], str):
            return {'error': 'Text is required and must be a non-empty string'}, 400

        if not (1 <= review_data.get('rating', 0) <= 5):
            return {'error': 'Rating must be an integer between 1 and 5'}, 400

        if not review_data.get('place_id'):
            return {'error': 'Place ID is required'}, 400

        # Vérifier si le lieu existe
        place = place_facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404

        # Vérifier si l'utilisateur est propriétaire du lieu
        if str(place.owner_id) == str(current_user['id']):
            return {'error': 'Cannot review your own place'}, 403

        # Vérifier si l'utilisateur a déjà laissé un avis sur ce lieu
        existing_review = review_facade.get_review_by_user_and_place(
            current_user['id'], review_data['place_id']
        )
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 403

        # Création de l'avis
        review_data['user_id'] = current_user['id']
        new_review = review_facade.create_review(review_data)

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Récupérer toutes les reviews"""
        try:
            reviews = review_facade.get_all_reviews()
            return [
                {'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id, 'place_id': r.place_id}
                for r in reviews
            ], 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.doc(security='jwt')
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Obtenir les détails d'une review par ID"""
        review = review_facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.doc(security='jwt')
    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized - Not the author')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Mettre à jour une review"""
        current_user = get_jwt_identity()
        review = review_facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if str(review.user_id) != str(current_user['id']):
            return {'error': 'Unauthorized - Not the review author'}, 403

        review_data = api.payload
        updated_review = review_facade.update_review(review_id, review_data)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
        }, 200

    @api.doc(security='jwt')
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Supprimer une review"""
        review = review_facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        review_facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Obtenir toutes les reviews d'un lieu spécifique"""
        place = place_facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = review_facade.get_reviews_by_place(place_id)
        return [
            {'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id, 'place_id': r.place_id}
            for r in reviews
        ], 200
