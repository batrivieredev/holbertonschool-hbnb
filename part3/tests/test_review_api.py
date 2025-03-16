import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1/reviews"

class TestReviewsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_review = {
            "text": "Super séjour !",
            "rating": 5,
            "place_id": "test_place_id"
        }
        cls.updated_review = {"text": "Séjour incroyable !", "rating": 4}

        response = requests.post(BASE_URL, json=cls.test_review)
        if response.status_code == 201:
            cls.review_id = response.json().get("id")
        else:
            cls.review_id = None

    def test_1_get_all_reviews(self):
        """Test récupération de tous les avis"""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200, response.text)

    def test_2_update_review(self):
        """Test mise à jour d'un avis"""
        if not self.review_id:
            self.skipTest("⚠️ Aucun avis enregistré, test annulé.")

        response = requests.put(f"{BASE_URL}/{self.review_id}", json=self.updated_review)
        self.assertEqual(response.status_code, 200, response.text)

if __name__ == "__main__":
    unittest.main()
