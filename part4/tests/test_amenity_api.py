import unittest
import requests
import uuid

BASE_URL = "http://localhost:5000/api/v1/amenities/"
AUTH_URL = "http://localhost:5000/api/v1/auth/login"
ADMIN_CREDENTIALS = {"email": "admin2@hbnb.io", "password": "admin12345"}

class TestAmenitiesAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Authenticate and create a test amenity with a unique name."""
        # Get admin token
        auth_response = requests.post(AUTH_URL, json=ADMIN_CREDENTIALS)
        if auth_response.status_code == 200:
            cls.token = auth_response.json().get("access_token")
            cls.headers = {"Authorization": f"Bearer {cls.token}", "Content-Type": "application/json"}
        else:
            cls.token = None
            cls.headers = {}

        # Generate a unique amenity name
        unique_name = f"Piscine_{uuid.uuid4().hex[:8]}"
        cls.test_amenity = {'name': unique_name}
        
        # Create test amenity
        response = requests.post(BASE_URL, json=cls.test_amenity, headers=cls.headers)
        if response.status_code == 201:
            cls.amenity_id = response.json().get("id")  # ✅ Store the created amenity ID
            cls.amenity_name = unique_name  # ✅ Store the unique name for validation
        else:
            cls.amenity_id = None
            cls.amenity_name = None

    def test_1_get_all_amenities(self):
        """Test retrieving all amenities."""
        response = requests.get(BASE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.amenity_name, str(response.json()))

    def test_2_get_amenity_by_id(self):
        """Test retrieving an amenity by ID."""
        if not self.amenity_id:
            self.skipTest("Test amenity was not created")
        response = requests.get(f"{BASE_URL}{self.amenity_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.amenity_name)

if __name__ == "__main__":
    unittest.main()
