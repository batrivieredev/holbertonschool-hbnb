#!/usr/bin/python3

"""
Modèle SQLAlchemy pour les équipements.
Définit la structure de données et les contraintes pour les équipements.

Table: amenities
Colonnes:
    - id (str): Identifiant unique UUID
    - name (str): Nom unique de l'équipement
    - created_at (datetime): Date de création
    - updated_at (datetime): Date de dernière modification
"""

from app.extensions import db
from app.models.BaseModel import BaseModel
import uuid

class Amenity(BaseModel):
    """Represents an amenity linked to a specific place."""

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Amenity {self.name}, Place ID: {self.place_id}>"