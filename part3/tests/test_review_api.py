import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1"
AUTH_URL = f"{BASE_URL}/auth/login"

class TestReviewsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up authentication, create a test place as admin, then create a review as another user"""

        cls.admin_credentials = {
            "email": "admin2@hbnb.io",
            "password": "admin12345"
        }

        cls.user_credentials = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test.user{uuid.uuid4()}@example.com",  # Unique email
            "password": "userpassword123"
        }

        # 🔹 1️⃣ Authenticate as Admin
        auth_response = requests.post(AUTH_URL, json=cls.admin_credentials)
        print(f"📌 DEBUG: Admin Auth Response Code: {auth_response.status_code}")
        print(f"📌 DEBUG: Admin Auth Response Body: {auth_response.text}")

        if auth_response.status_code == 200:
            cls.admin_token = auth_response.json().get("access_token")
        else:
            cls.admin_token = None
            raise unittest.SkipTest("Admin authentication failed. Cannot proceed.")

        # 🔹 2️⃣ Create a test place (as admin)
        headers = {"Authorization": f"Bearer {cls.admin_token}"}
        test_place = {
            "title": "Test Place",
            "city_id": "test_city_id",
            "description": "A great test place",
            "price": 100,
            "latitude": 48.8566,
            "longitude": 2.3522
        }
        place_response = requests.post(f"{BASE_URL}/places", json=test_place, headers=headers)

        print(f"📌 DEBUG: Create Place Response Code: {place_response.status_code}")
        print(f"📌 DEBUG: Create Place Response Body: {place_response.text}")

        if place_response.status_code == 201:
            cls.place_id = place_response.json().get("id")
            print(f"✅ Place Created with ID: {cls.place_id}")
        else:
            cls.place_id = None
            raise unittest.SkipTest("Place creation failed. Cannot proceed.")

        # 🔹 3️⃣ Create a separate user for review creation
        user_creation_response = requests.post(f"{BASE_URL}/users", json=cls.user_credentials, headers=headers)

        print(f"📌 DEBUG: Create User Response Code: {user_creation_response.status_code}")
        print(f"📌 DEBUG: Create User Response Body: {user_creation_response.text}")

        if user_creation_response.status_code == 201:
            cls.user_id = user_creation_response.json().get("id")
            print(f"✅ User Created with ID: {cls.user_id}")
        else:
            cls.user_id = None
            raise unittest.SkipTest("User creation failed. Cannot proceed.")

        # 🔹 4️⃣ Authenticate as the new user
        user_auth_response = requests.post(AUTH_URL, json={
            "email": cls.user_credentials["email"],
            "password": cls.user_credentials["password"]
        })

        print(f"📌 DEBUG: User Auth Response Code: {user_auth_response.status_code}")
        print(f"📌 DEBUG: User Auth Response Body: {user_auth_response.text}")

        if user_auth_response.status_code == 200:
            cls.user_token = user_auth_response.json().get("access_token")
        else:
            cls.user_token = None
            raise unittest.SkipTest("User authentication failed. Cannot proceed.")

        # 🔹 5️⃣ Create a review using the new user
        cls.test_review = {
            "text": "Super séjour !",
            "rating": 5,
            "place_id": cls.place_id
        }
        cls.updated_review = {"text": "Séjour incroyable !", "rating": 4}

        review_headers = {"Authorization": f"Bearer {cls.user_token}"}
        response = requests.post(f"{BASE_URL}/reviews", json=cls.test_review, headers=review_headers)

        print(f"📌 DEBUG: Create Review Response Code: {response.status_code}")
        print(f"📌 DEBUG: Create Review Response Body: {response.text}")

        if response.status_code == 201:
            cls.review_id = response.json().get("id")
            print(f"✅ Review Created with ID: {cls.review_id}")
        else:
            cls.review_id = None
            print("❌ Review Creation Failed! Skipping update test.")

    def test_1_get_all_reviews(self):
        """Test récupération de tous les avis"""
        response = requests.get(f"{BASE_URL}/reviews")
        self.assertEqual(response.status_code, 200, response.text)

    def test_2_update_review(self):
        """Test mise à jour d'un avis"""
        if not self.review_id:
            self.skipTest("⚠️ Aucun avis enregistré, test annulé.")

        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.put(f"{BASE_URL}/reviews/{self.review_id}", json=self.updated_review, headers=headers)
        self.assertEqual(response.status_code, 200, response.text)

if __name__ == "__main__":
    unittest.main()
