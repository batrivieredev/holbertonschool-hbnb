from app.models.review import Review
from app.persistence.repository import InMemoryRepository


class ReviewFacade:
    def __init__(self):
        self.review_repo = InMemoryRepository()


def create_review(self, review_data):
    '''Créer une nouvelle review'''
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
