"""API des réservations pour l'application HBNB"""
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models.booking import Booking
from app.models.place import Place
from app.models.user import User

# Création du blueprint des réservations
bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/places/<string:place_id>/bookings', methods=['POST'])
@jwt_required()
def create_booking(place_id):
    """Crée une nouvelle réservation pour un lieu"""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Lieu non trouvé'}), 404

        # Vérifie que l'utilisateur ne réserve pas son propre lieu
        if place.owner_id == current_user_id:
            return jsonify({'error': 'Vous ne pouvez pas réserver votre propre lieu'}), 400

        data = request.get_json()

        # Validation des dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except (ValueError, KeyError):
            return jsonify({'error': 'Dates invalides'}), 400

        # Vérifie si les dates sont disponibles
        existing_booking = Booking.query.filter(
            Booking.place_id == place_id,
            Booking.status != 'cancelled',
            ((Booking.start_date <= end_date) & (Booking.end_date >= start_date))
        ).first()

        if existing_booking:
            return jsonify({'error': 'Ces dates ne sont pas disponibles'}), 400

        # Crée la réservation
        booking = Booking(
            place_id=place_id,
            user_id=current_user_id,
            start_date=start_date,
            end_date=end_date,
            message=data.get('message', ''),
            status='pending'
        )

        booking.validate()
        booking.save()

        # TODO: Envoyer un email au propriétaire

        return jsonify(booking.to_dict()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/places/<string:place_id>/bookings', methods=['GET'])
@jwt_required()
def get_place_bookings(place_id):
    """Récupère les réservations d'un lieu"""
    try:
        current_user_id = get_jwt_identity()
        place = Place.query.get(place_id)

        if not place:
            return jsonify({'error': 'Lieu non trouvé'}), 404

        # Seul le propriétaire peut voir toutes les réservations
        if place.owner_id != current_user_id:
            return jsonify({'error': 'Non autorisé'}), 403

        bookings = Booking.query.filter_by(place_id=place_id).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/bookings/<string:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    """Met à jour le statut d'une réservation"""
    try:
        current_user_id = get_jwt_identity()
        booking = Booking.query.get(booking_id)

        if not booking:
            return jsonify({'error': 'Réservation non trouvée'}), 404

        # Vérifie que c'est bien le propriétaire qui met à jour
        if booking.place.owner_id != current_user_id:
            return jsonify({'error': 'Non autorisé'}), 403

        data = request.get_json()
        status = data.get('status')

        if status not in ['confirmed', 'cancelled']:
            return jsonify({'error': 'Statut invalide'}), 400

        booking.status = status
        booking.save()

        # TODO: Envoyer un email au locataire

        return jsonify(booking.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/users/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    """Récupère les réservations de l'utilisateur connecté"""
    try:
        current_user_id = get_jwt_identity()
        bookings = Booking.query.filter_by(user_id=current_user_id).all()
        return jsonify([booking.to_dict() for booking in bookings]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
