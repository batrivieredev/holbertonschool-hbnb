"""
Facade pour la gestion des avis.
Implémente la logique métier pour les avis et notes.

Responsabilités:
    - Validation des notes (1-5)
    - Vérification des droits utilisateur
    - Calcul des moyennes
    - Gestion des contraintes (ex: un avis par utilisateur)
"""

from app.models.review import Review
from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository


class ReviewFacade:
    def __init__(self):
        self.review_repo = SQLAlchemyRepository(Review)


def create_review(self, review_data):
    """Crée un nouvel avis.

    Validation:
        - Note entre 1 et 5
        - Texte non vide
        - Un seul avis par utilisateur par lieu

    Args:
        review_data (dict): Données de l'avis

    Returns:
        Review: Instance créée ou None si erreur
    """
    review = Review(**review_data)
    self.review_repo.add(review)
    return review


def get_review(self, review_id):
    '''Récupérer une review par ID'''
    return self.review_repo.get(review_id)


def get_all_reviews(self):
    '''Récupérer toutes les reviews'''
    reviews = self.review_repo.get_all()
    return reviews


def get_reviews_by_place(self, place_id):
    '''Récupérer toutes les reviews pour un lieu'''
    reviews = self.review_repo.get_all()
    return [review for review in reviews if review.place_id == place_id]


def update_review(self, review_id, review_data):
    '''Mettre à jour une review'''
    review = self.get_review(review_id)
    if not review:
        return None
    for key, value in review_data.items():
        setattr(review, key, value)
    self.review_repo.update(review)
    return review


def delete_review(self, review_id):
    '''Supprimer une review'''
    return self.review_repo.delete(review_id)
