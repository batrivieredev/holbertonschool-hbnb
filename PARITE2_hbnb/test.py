#!/usr/bin/python3

import unittest
from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)


class TestPlace(unittest.TestCase):
    def test_place_creation(self):
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        place = Place(title="Cozy Apartment", description="A nice place to stay",
                      price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)

        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.owner, owner)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)

    def test_add_review(self):
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        place = Place(title="Cozy Apartment", description="A nice place to stay",
                      price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
        review = Review(place_id=place.id, user_id=owner.id,
                        text="Great stay!", rating=4)
        place.add_review(review)

        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")

    def test_add_amenity(self):
        owner = User(first_name="Alice", last_name="Smith",
                     email="alice.smith@example.com")
        place = Place(title="Cozy Apartment", description="A nice place to stay",
                      price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
        amenity = Amenity(name="Wi-Fi")
        place.add_amenity(amenity)

        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(place.amenities[0].name, "Wi-Fi")


class TestReview(unittest.TestCase):
    def test_review_creation(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        place = Place(title="Beach House", description="A lovely beach house",
                      price=200.0, latitude=34.0194, longitude=-118.4912, owner=user)
        review = Review(place_id=place.id, user_id=user.id,
                        text="Amazing experience!", rating=5, place=place, user=user)
        self.assertEqual(review.text, "Amazing experience!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, place)
        self.assertEqual(review.user, user)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)


class TestAmenity(unittest.TestCase):
    def test_amenity_creation(self):
        amenity = Amenity(name="Parking")
        self.assertEqual(amenity.name, "Parking")
        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)


if __name__ == "__main__":
    unittest.main()
