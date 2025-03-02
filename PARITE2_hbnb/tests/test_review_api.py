import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/reviews/"

class TestReviewsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Créer une review test."""
        cls.test_review = {
            "text": "Super endroit!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }

        response = requests.post(BASE_URL, json=cls.test_review)
        if response.status_code == 201:
            cls.review_id = response.json().get("id")
        else:
            cls.review_id = None

    def test_1_create_review(self):
        """Test de la création d'une review."""
        response = requests.post(BASE_URL, json=self.test_review)
        self.assertEqual(response.status_code, 201)

    def test_2_get_all_reviews(self):
        """Test de récupération de toutes les reviews."""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_3_get_review_by_id(self):
        """Test de récupération d'une review par ID."""
        if not self.review_id:
            self.skipTest("Review non créée")
        response = requests.get(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)

    def test_4_update_review(self):
        """Test de mise à jour d'une review."""
        if not self.review_id:
            self.skipTest("Review non créée")
        updated_data = {"text": "Endroit correct.", "rating": 3}
        response = requests.put(f"{BASE_URL}{self.review_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)

    def test_5_delete_review(self):
        """Test de suppression d'une review."""
        if not self.review_id:
            self.skipTest("Review non créée")
        response = requests.delete(f"{BASE_URL}{self.review_id}")
        self.assertEqual(response.status_code, 200)

    def test_6_get_nonexistent_review(self):
        """Test de récupération d'une review inexistante."""
        response = requests.get(f"{BASE_URL}nonexistent-id")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
