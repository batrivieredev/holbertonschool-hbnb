from app.models.BaseModel import BaseModel
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None):
        super().__init__()
        self.title = title[:100]  # Max length 100
        self.description = description
        self.price = max(price, 0.0)  # Ensure price is positive
        self.latitude = max(min(latitude, 90.0), -90.0)  # Validate range
        self.longitude = max(min(longitude, 180.0), -180.0)  # Validate range
        self.owner = owner  # Expecting a User instance
        self.reviews = []  # Store related reviews
        self.amenities = amenities if amenities else []  # Store related amenities

    def add_review(self, review):
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity)