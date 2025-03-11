#!/usr/bin/python3

"""
Modèle SQLAlchemy pour les lieux.
Gère les propriétés et locations disponibles.

Relations:
    - User: Propriétaire du lieu
    - Amenity: Équipements disponibles
    - Review: Avis reçus

Fonctionnalités:
    - Géolocalisation (lat/long)
    - Tarification
    - Gestion des disponibilités
"""

from app.extensions import db
from app.models.BaseModel import BaseModel

class Place(BaseModel):
    """Représente un lieu dans la base de données.

    Attributes:
        title (str): Titre de l'annonce
        description (Text): Description détaillée
        price (float): Prix par nuit
        latitude (float): Coordonnée GPS
        longitude (float): Coordonnée GPS
        owner_id (str): Référence vers le propriétaire

    Relations:
        owner: Propriétaire du lieu
        amenities: Liste des équipements
        reviews: Avis reçus
    """
    __tablename__ = 'places'  # ✅ Define table name

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # ✅ Foreign key reference

    owner = db.relationship('User', backref='places', lazy=True)  # ✅ Define relationship

    def __repr__(self):
        return f"<Place {self.title}>"

