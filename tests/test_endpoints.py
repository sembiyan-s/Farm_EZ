import unittest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

class TestFarmerAPI(unittest.TestCase):
    # We use a distinct mobile number for testing to avoid collisions with manual testing
    TEST_MOBILE = "9999988888"
    
    def setUp(self):
        # Small delay to ensure server processes requests
        time.sleep(0.1)

    def test_01_create_farmer(self):
        print("\nTesting Create Farmer...")
        
        # Cleanup: Delete if exists to ensure clean state
        requests.delete(f"{BASE_URL}/delete-basic-farmer/{self.TEST_MOBILE}")
        
        payload = {
            "name": "Test Farmer",
            "age": 30,
            "address": {
                "street": "Test Street",
                "village": "Test Village",
                "city": "Test City",
                "state": "Test State",
                "pincode": 600000
            },
            "mobile_number": self.TEST_MOBILE
        }
        
        response = requests.post(f"{BASE_URL}/create-basic-farmer", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json()["status"])

    def test_02_get_farmer(self):
        print("\nTesting Get Farmer...")
        response = requests.get(f"{BASE_URL}/get-basic-farmer/{self.TEST_MOBILE}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Farmer")
        self.assertEqual(data["mobile_number"], self.TEST_MOBILE)

    def test_03_update_farmer(self):
        print("\nTesting Update Farmer...")
        update_payload = {
            "name": "Updated Test Farmer",
            "age": 31
        }
        response = requests.patch(f"{BASE_URL}/update-basic-farmer/{self.TEST_MOBILE}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        get_response = requests.get(f"{BASE_URL}/get-basic-farmer/{self.TEST_MOBILE}")
        self.assertEqual(get_response.json()["name"], "Updated Test Farmer")
        self.assertEqual(get_response.json()["age"], 31)

    def test_04_update_farmer_invalid_field(self):
        print("\nTesting Update Farmer with Invalid Field...")
        # Should fail because we set extra="forbid"
        payload = {
            "name": "Hacker",
            "mobile_number": "0000000000" # Not allowed
        }
        response = requests.patch(f"{BASE_URL}/update-basic-farmer/{self.TEST_MOBILE}", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_05_create_crop(self):
        print("\nTesting Create Crop...")
        crop_payload = {
            "crop_name": "Wheat",
            "crop_variant": "Kalyan Sona",
            "crop_area": 5,
            "cultivation_date": "2023-11-01",
            "type_of_cultivation": "Organic",
            "harvest_date": "2024-04-01",
            "location": ["Field A", "Field B"]
        }
        # Note: Query param mobile_number is expected by the endpoint logic if I recall correctly
        # Let's double check main.py signature: async def create_crop(mobile_number: str, crop: Crop):
        # This means mobile_number is a Query Parameter.
        
        response = requests.post(
            f"{BASE_URL}/create-crop", 
            params={"mobile_number": self.TEST_MOBILE}, 
            json=crop_payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Crop added", response.json()["message"])
        
        # Verify crop addition via Get (if the model returns it)
        # The Current Get endpoint returns doc.to_dict(). If crops are added, they should appear.
        get_response = requests.get(f"{BASE_URL}/get-basic-farmer/{self.TEST_MOBILE}")
        self.assertIn("crops", get_response.json())
        self.assertEqual(len(get_response.json()["crops"]), 1)
        self.assertEqual(get_response.json()["crops"][0]["crop_name"], "Wheat")

    def test_06_delete_farmer(self):
        print("\nTesting Delete Farmer...")
        response = requests.delete(f"{BASE_URL}/delete-basic-farmer/{self.TEST_MOBILE}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json()["message"])
        
        # Verify deletion
        get_response = requests.get(f"{BASE_URL}/get-basic-farmer/{self.TEST_MOBILE}")
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    # Custom runner to ensure sequential execution by name sorting is standard in unittest, 
    # but strictly speaking tests should be independent. 
    # Here they depend on state (Create -> Get -> Update), so we name them carefully.
    unittest.main()
