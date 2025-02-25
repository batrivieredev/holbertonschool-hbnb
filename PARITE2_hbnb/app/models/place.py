#!/usr/bin/env python3


import uuid
from datetime import datetime
from app.models.amenity import Amenity
from app.models.review import Review


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

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
