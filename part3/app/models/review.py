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

    def __repr__(self):
        return f"<Review {self.rating}/5 for Place {self.place_id}>"
