import unittest
import requests
import time
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

class TestJobAPI(unittest.TestCase):
    JOB_ID = None
    
    @classmethod
    def setUpClass(cls):
        # Ensure clean state or setup global configs if needed
        pass

    def test_01_create_job(self):
        print("\nTesting Create Job...")
        payload = {
            "job_title": "Shared Integration Job",
            "job_description": "Job for sequential testing",
            "job_location": "Test Valley",
            "job_skills": ["Testing"],
            "job_type": "Full-time",
            "job_salary": 1000,
            "job_requirements": ["None"],
            "job_posted_date": "2023-12-01",
            "posted_by_name": "Test Runner",
            "posted_by_mobile": "1231231234"
        }
        
        response = requests.post(f"{BASE_URL}/create-job", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("job_id", json_data)
        
        # Store for other tests
        TestJobAPI.JOB_ID = json_data["job_id"]
        print(f"Created Job ID: {TestJobAPI.JOB_ID}")

    def test_02_get_job(self):
        print("\nTesting Get Job...")
        self.assertIsNotNone(TestJobAPI.JOB_ID, "Job ID not set. Did create test fail?")
        
        response = requests.get(f"{BASE_URL}/get-job/{TestJobAPI.JOB_ID}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["job_title"], "Shared Integration Job")
        self.assertEqual(data["job_id"], TestJobAPI.JOB_ID)

    def test_03_update_job_contact(self):
        print("\nTesting Update Job Contact...")
        self.assertIsNotNone(TestJobAPI.JOB_ID, "Job ID not set.")

        update_payload = {
            "posted_by_name": "Updated Runner",
            "posted_by_mobile": "9999999999"
        }
        response = requests.patch(f"{BASE_URL}/update-job/{TestJobAPI.JOB_ID}", json=update_payload)
        self.assertEqual(response.status_code, 200)

        # Verify
        get_response = requests.get(f"{BASE_URL}/get-job/{TestJobAPI.JOB_ID}")
        self.assertEqual(get_response.json()["posted_by_name"], "Updated Runner")
        self.assertEqual(get_response.json()["posted_by_mobile"], "9999999999")

    def test_04_delete_job(self):
        print("\nTesting Delete Job...")
        self.assertIsNotNone(TestJobAPI.JOB_ID, "Job ID not set.")
        
        response = requests.delete(f"{BASE_URL}/delete-job/{TestJobAPI.JOB_ID}")
        self.assertEqual(response.status_code, 200)
        
        # Verify 404
        get_response = requests.get(f"{BASE_URL}/get-job/{TestJobAPI.JOB_ID}")
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
