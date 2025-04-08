#!/usr/bin/python3

import uuid
from datetime import datetime
from app.extensions import db

"""
Modèle de base pour tous les objets de l'application.
Fournit les champs communs et fonctionnalités partagées.

Fonctionnalités:
    - Génération automatique d'ID unique (UUID)
    - Horodatage automatique (création/modification)
    - Méthodes communes de persistence
"""

class BaseModel(db.Model):
    """Classe de base abstraite pour tous les modèles.
    Hérite de db.Model pour fournir la fonctionnalité SQLAlchemy.

    Attributes:
        id (str): Identifiant unique UUID v4
        created_at (datetime): Date de création automatique
        updated_at (datetime): Date de dernière modification
    """
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this base class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the instance to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Met à jour l'instance avec les données fournies.

        Args:
            data (dict): Dictionnaire des champs à mettre à jour

        Notes:
            - Mise à jour automatique de updated_at
            - Ignore les champs qui n'existent pas
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
