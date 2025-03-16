import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1"

class TestAdminAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Authentifier l'admin et stocker le token"""
        cls.admin_login_data = {"email": "admin@hbnb.io", "password": "admin1234"}
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json=cls.admin_login_data)
        if login_response.status_code == 200:
            cls.admin_token = login_response.json().get("access_token")
            print("✅ Admin login successful!")
        else:
            cls.admin_token = None
            print("❌ Failed to log in as admin:", login_response.text)

        # Créer un utilisateur test
        cls.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        user_response = requests.post(f"{BASE_URL}/users/", json=cls.user_data)
        if user_response.status_code in [201, 400]:  # 400 if already exists
            print("✅ Test user created or already exists.")
        else:
            print("❌ Failed to create test user:", user_response.text)

        # Connexion utilisateur test
        user_login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": cls.user_data["email"],
            "password": cls.user_data["password"]
        })
        if user_login_response.status_code == 200:
            cls.user_token = user_login_response.json().get("access_token")
            print("✅ Normal user login successful!")
        else:
            cls.user_token = None
            print("❌ Failed to log in as normal user:", user_login_response.text)

    def test_1_create_user_as_admin(self):
        """Admin peut créer un utilisateur"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        new_user = {
            "email": "newadminuser@example.com",
            "first_name": "New",
            "last_name": "Admin",
            "password": "securepassword"
        }
        response = requests.post(f"{BASE_URL}/users/", json=new_user, headers=headers)
        
        print("🛑 DEBUG: Response from API:", response.text)
        self.assertEqual(response.status_code, 201)

    def test_3_modify_user_as_admin(self):
        """Admin peut modifier un utilisateur"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(f"{BASE_URL}/users/{self.user_data['email']}", json={"first_name": "Updated"}, headers=headers)
        
        print("🛑 DEBUG:", response.text)
        self.assertEqual(response.status_code, 200)

    def test_5_add_amenity_as_admin(self):
        """Admin peut ajouter une commodité"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        amenity_data = {"name": f"Pool {requests.get(BASE_URL).status_code}"}  # Unique name
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=headers)

        print("🛑 DEBUG:", response.text)
        self.assertEqual(response.status_code, 201)

    def test_7_modify_amenity_as_admin(self):
        """Admin peut modifier une commodité"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Fetch a valid amenity ID first
        amenities = requests.get(f"{BASE_URL}/amenities/", headers=headers).json()
        if not amenities:
            self.skipTest("⚠️ No amenities available to modify!")
        
        amenity_id = amenities[0]["id"]
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json={"name": "Updated Pool"}, headers=headers)

        print("🛑 DEBUG:", response.text)
        self.assertEqual(response.status_code, 200)

    def test_9_admin_can_modify_any_place(self):
        """Admin peut modifier un lieu"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Fetch a valid place ID first
        places = requests.get(f"{BASE_URL}/places/", headers=headers).json()
        if not places:
            self.skipTest("⚠️ No places available to modify!")

        place_id = places[0]["id"]
        response = requests.put(f"{BASE_URL}/places/{place_id}", json={"name": "Updated Place"}, headers=headers)

        print("🛑 DEBUG:", response.text)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
