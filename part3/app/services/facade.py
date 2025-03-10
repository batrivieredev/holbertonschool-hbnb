from app.services.UsersFacade import UsersFacade
from app.services.AmenityFacade import AmenityFacade
from app.services.PlaceFacade import PlaceFacade
from app.services.ReviewFacade import ReviewFacade


class HBnBFacade(UsersFacade, AmenityFacade):
    def __init__(self):
        super().__init__()
        self.user_repo = UsersFacade()
        self.place_repo = PlaceFacade()
        self.review_repo = ReviewFacade()
        self.amenity_repo = AmenityFacade()
