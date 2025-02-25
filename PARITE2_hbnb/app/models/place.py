#!/usr/bin/env python3

from app.models.BaseModel import BaseModel
from app.models.amenity import Amenity
from app.models.review import Review

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title[:100]  # Max length 100
        self.description = description
        self.price = max(price, 0.0)  # Ensure price is positive
        self.latitude = max(min(latitude, 90.0), -90.0)  # Validate range
        self.longitude = max(min(longitude, 180.0), -180.0)  # Validate range
        self.owner = owner  # Expecting a User instance
        self.reviews = []  # Store related reviews
        self.amenities = []  # Store related amenities

# In case we want to add a review to a place, we can use the add_review method.
    def add_review(self, review):
        if isinstance(review, Review):
            self.reviews.append(review)

# In case we want to add an amenity to a place, we can use the add_amenity method.
    def add_amenity(self, amenity):
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity)
