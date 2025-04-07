import unittest
import requests
import uuid  # ✅ Import UUID for unique titles

BASE_URL = "http://localhost:5000/api/v1/places"
AUTH_URL = "http://localhost:5000/api/v1/auth/login"
ADMIN_CREDENTIALS = {"email": "admin2@hbnb.io", "password": "admin12345"}

class TestPlacesAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Authenticate and create a test place with a unique title"""
        # ✅ Get admin token
        auth_response = requests.post(AUTH_URL, json=ADMIN_CREDENTIALS)
        if auth_response.status_code == 200:
            cls.token = auth_response.json().get("access_token")
            cls.headers = {"Authorization": f"Bearer {cls.token}", "Content-Type": "application/json"}
        else:
            cls.token = None
            cls.headers = {}

        # ✅ Generate a unique title to avoid conflicts
        unique_id = uuid.uuid4().hex[:6]  # Short UUID fragment
        cls.test_place = {
            "title": f"Appartement cosy {unique_id}",
            "description": "Très bel appartement en centre-ville",
            "price": 100.00,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": "36c9050e-ddd3-4c3b-9731-9f487208bbc1"  # Set a valid owner_id
        }

        response = requests.post(BASE_URL, json=cls.test_place, headers=cls.headers)
        if response.status_code == 201:
            cls.place_id = response.json().get("id")  # ✅ Store the created place ID
            print(f"✅ Place created with ID: {cls.place_id}")
        else:
            cls.place_id = None
            print(f"❌ Failed to create place: {response.status_code} {response.text}")

    def test_1_get_all_places(self):
        """✅ Test retrieving all places"""
        response = requests.get(BASE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_2_get_place_details(self):
        """✅ Test retrieving details of a place"""
        if not self.place_id:
            self.skipTest("Test place was not created")
        response = requests.get(f"{BASE_URL}/{self.place_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_3_update_place(self):
        """✅ Test updating a place (with authentication)"""
        if not self.place_id:
            self.skipTest("Test place was not created")
        
        updated_place = {"title": f"Appartement luxueux {uuid.uuid4().hex[:6]}"}
        response = requests.put(f"{BASE_URL}/{self.place_id}", json=updated_place, headers=self.headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
