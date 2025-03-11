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

class Amenity(BaseModel):
    """Représente un équipement dans la base de données.

    Attributes:
        name (str): Nom de l'équipement, unique et obligatoire
    """
    __tablename__ = 'amenities'  # ✅ Define table name

    name = db.Column(db.String(50),
                    nullable=False,
                    unique=True,
                    comment="Nom unique de l'équipement, max 50 caractères")

    def __repr__(self):
        return f"<Amenity {self.name}>"
