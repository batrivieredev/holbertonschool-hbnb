import unittest
import requests

BASE_URL = "http://localhost:5000/reviews/"

class TestReviewAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_review = {
            'text': 'Super endroit !',
            'rating': 5,
            'place_id': 'test_place_id'
        }
        response = requests.post(BASE_URL, json=cls.test_review)
        if response.status_code == 201:
            cls.review_id = response.json().get("id")

    def test_1_get_review_by_id(self):
        """Test de récupération d'une review par ID."""
        response = requests.get(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)

    def test_2_delete_review(self):
        """Test de suppression d'une review."""
        response = requests.delete(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
