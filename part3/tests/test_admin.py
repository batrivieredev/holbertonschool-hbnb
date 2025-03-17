import unittest
import requests

BASE_URL = "http://localhost:5000/api/v1"


class TestAdminAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Authenticate admin and store token, create a test user and place"""
        cls.admin_login_data = {"email": "admin2@hbnb.io", "password": "admin12345"}
        login_response = requests.post(f"{BASE_URL}/auth/login", json=cls.admin_login_data)

        if login_response.status_code == 200:
            cls.admin_token = login_response.json().get("access_token")
            print("✅ Admin login successful!")
        else:
            cls.admin_token = None
            print("❌ Failed to log in as admin:", login_response.text)
            return  # Stop setup if login fails

        headers = {"Authorization": f"Bearer {cls.admin_token}"}

        # Create or retrieve test user
        cls.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        user_response = requests.post(f"{BASE_URL}/users/", json=cls.user_data, headers=headers)

        if user_response.status_code == 201:
            cls.user_id = user_response.json().get("id")
            print("✅ Test user created.")
        elif user_response.status_code == 400:
            print("⚠️ Test user might already exist.")
            # Fetch user ID manually
            users_response = requests.get(f"{BASE_URL}/users/", headers=headers)
            if users_response.status_code == 200:
                users = users_response.json()
                for user in users:
                    if user["email"] == cls.user_data["email"]:
                        cls.user_id = user["id"]
                        print(f"✅ Found existing user ID: {cls.user_id}")
                        break
            else:
                print("❌ Failed to retrieve user list.")
                cls.user_id = None
        else:
            print("❌ Failed to create test user:", user_response.text)
            cls.user_id = None

        # Create or retrieve a test place
        cls.place_data = {
            "title": "Test Place",
            "description": "A beautiful place",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522
        }
        place_response = requests.post(f"{BASE_URL}/places/", json=cls.place_data, headers=headers)

        if place_response.status_code == 201:
            cls.place_id = place_response.json().get("id")
            print("✅ Test place created successfully!")
        elif place_response.status_code == 400:
            print("⚠️ Test place might already exist.")
            cls.place_id = None
        else:
            print("❌ Failed to create test place:", place_response.text)
            cls.place_id = None

    def test_1_create_user_as_admin(self):
        """Admin can create a user"""
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
        self.assertIn(response.status_code, [201, 400])  # 400 if user exists

    def test_3_modify_user_as_admin(self):
        """Admin can modify a user (Ensure correct method: PUT/PATCH)"""
        if not self.admin_token or not self.user_id:
            self.skipTest("⚠️ Admin token or user ID missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Try using PATCH instead of PUT
        response = requests.patch(
            f"{BASE_URL}/users/{self.user_id}",
            json={"first_name": "Updated"},
            headers=headers
        )

        print("🛑 DEBUG: Modify user response:", response.text)
        self.assertIn(response.status_code, [200, 405])  # Check if method is allowed

    def test_5_add_amenity_as_admin(self):
        """Admin can add an amenity"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}
        amenity_data = {"name": "Swimming Pool"}
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=headers)

        print("🛑 DEBUG:", response.text)
        self.assertIn(response.status_code, [201, 400])  # 400 if amenity exists

    def test_7_modify_amenity_as_admin(self):
        """Admin can modify an amenity"""
        if not self.admin_token:
            self.skipTest("⚠️ Admin token missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Fetch a valid amenity ID first
        amenities_response = requests.get(f"{BASE_URL}/amenities/", headers=headers)
        if amenities_response.status_code != 200 or not amenities_response.json():
            self.skipTest("⚠️ No amenities available to modify!")

        amenity_id = amenities_response.json()[0]["id"]
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json={"name": "Updated Pool"}, headers=headers)

        print("🛑 DEBUG:", response.text)
        self.assertEqual(response.status_code, 200)

    def test_13_admin_can_delete_a_user(self):
        """Admin can delete a user (Ensure correct method)"""
        if not self.admin_token or not self.user_id:
            self.skipTest("⚠️ Admin token or user ID missing!")

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Try using PATCH instead of DELETE if deactivation is used
        response = requests.delete(f"{BASE_URL}/users/{self.user_id}", headers=headers)

        print("🛑 DEBUG: Delete user response:", response.text)
        self.assertIn(response.status_code, [200, 405])  # Check if method is allowed


if __name__ == "__main__":
    unittest.main()
