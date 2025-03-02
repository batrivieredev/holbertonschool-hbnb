from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class ReviewFacade:
    def __init__(self):
        self.review_repo = InMemoryRepository()

    def create_review(self, review_data):
        if not review_data.get('user_id') or not review_data.get('place_id'):
            raise ValueError("user_id et place_id sont requis")
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("La note doit être entre 1 et 5")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [review for review in reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review.id, review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
