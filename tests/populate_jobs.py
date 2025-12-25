import requests
import random
import string
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_mobile():
    return str(random.randint(6000000000, 9999999999))

def create_random_job(index):
    # Job ID is now auto-generated, so we don't send it.
    job_title = random.choice(["Farm Hand", "Tractor Driver", "Harvester", "Supervisor", "Irrigation Specialist"])
    
    payload = {
        "job_title": job_title,
        "job_description": f"Description for {job_title}",
        "job_location": random.choice(["Village A", "Village B", "City X", "City Y"]),
        "job_skills": random.sample(["Harvesting", "Driving", "Digging", "Management", "Plowing"], k=2),
        "job_type": random.choice(["Full-time", "Part-time", "Contract"]),
        "job_salary": random.randint(300, 1000),
        "job_requirements": ["Requirement 1", "Requirement 2"],
        "job_posted_date": str(date.today()),
        "posted_by_name": f"Farmer {random_string(3)}",
        "posted_by_mobile": random_mobile()
    }
    
    try:
        response = requests.post(f"{BASE_URL}/create-job", json=payload)
        if response.status_code == 200:
            print(f"Created Job {index}: Success ID={response.json().get('job_id')}")
        else:
            print(f"Created Job {index}: Failed {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error creating Job {index}: {e}")

if __name__ == "__main__":
    print("Creating 10 random jobs...")
    for i in range(10):
        create_random_job(i)
