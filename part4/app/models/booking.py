"""Modèle de réservation pour l'application HBNB"""
from app.extensions import db
from app.models.BaseModel import BaseModel

class Booking(BaseModel):
    """Modèle pour les réservations de logements"""

    __tablename__ = 'bookings'

    # Informations de réservation
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    message = db.Column(db.Text)  # Message du locataire pour le propriétaire

    # Relations
    place = db.relationship('Place', backref=db.backref('bookings', lazy=True))
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

    def validate(self):
        """Valide les données de la réservation"""
        if not self.start_date:
            raise ValueError("La date de début est requise")
        if not self.end_date:
            raise ValueError("La date de fin est requise")
        if self.start_date > self.end_date:
            raise ValueError("La date de début doit être antérieure à la date de fin")

    def to_dict(self):
        """Convertit la réservation en dictionnaire"""
        booking_dict = super().to_dict()
        booking_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'message': self.message,
            'place': {
                'id': self.place.id,
                'title': self.place.title
            } if self.place else None,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            } if self.user else None
        })
        return booking_dict

    def __repr__(self):
        return f"<Booking {self.id} - Place: {self.place_id}, User: {self.user_id}>"
