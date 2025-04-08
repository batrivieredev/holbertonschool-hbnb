#!/usr/bin/python3

"""
Modèle SQLAlchemy pour les avis utilisateurs.
Gère les évaluations et commentaires sur les lieux.

Relations:
    - User: Auteur de l'avis
    - Place: Lieu concerné par l'avis

Contraintes:
    - Note entre 1 et 5
    - Texte obligatoire
    - Un seul avis par utilisateur par lieu
"""

from app.extensions import db
from app.models.BaseModel import BaseModel

class Review(BaseModel):
    """Représente un avis dans la base de données.

    Attributes:
        text (Text): Contenu de l'avis
        rating (int): Note sur 5
        user_id (str): Référence vers l'auteur
        place_id (str): Référence vers le lieu

    Relations:
        user: Auteur de l'avis
        place: Lieu évalué
    """
    __tablename__ = 'reviews'  # ✅ Define table name

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place = db.relationship('Place', back_populates='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)  # ✅ Define relationship

    def to_dict(self):
        """Convert model instance to dict."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            } if self.user else None
        }

    def __repr__(self):
        return f"<Review {self.rating}/5 for Place {self.place_id}>"
