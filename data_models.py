from pydantic import BaseModel
from typing import Optional , Literal , List
from datetime import date

# data models for farmer 
class Address(BaseModel):
    street:Optional[str] = None
    village:str
    city:str
    state:str
    pincode:int

class Farmer(BaseModel):
    name:str
    age:int
    address: Address
    mobile_number:str

class Crop(BaseModel):
    crop_name: str
    crop_variant: str
    crop_area: int
    cultivation_date: str   
    type_of_cultivation: Literal["Organic", "Non-Organic"]
    harvest_date: str       
    location: List[str]


class TotalCrop(BaseModel):
    crop : List[Crop]

class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

    class Config:
        extra = "forbid"
    

# data models for labour

class LabourProfile(BaseModel):
    name: str
    mobile_no: str
    skills: List[str] # e.g., ["harvest", "tractor driver", "JCB"]
    location: str
    age: int
    # expected_daily_wage: float
    # willing_to_stay_at_work: bool = False
    # experience_years: int
    # rating: Optional[float] = 0.0
    # feedback: Optional[List[str]] = []

# labour update model
class LabourProfileUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    age: Optional[int] = None

    class Config:
        extra = "forbid"

# data models for job

class JobCreate(BaseModel):
    job_title: str
    job_description: str
    job_location: str
    job_skills: List[str]
    job_type: Literal["Full-time", "Part-time", "Contract"]
    job_salary: int
    job_requirements: List[str]
    job_posted_date: date
    posted_by_name: str
    posted_by_mobile: str

class Job(JobCreate):
    job_id: str

class JobUpdate(BaseModel):
    job_title: Optional[str] = None
    job_description: Optional[str] = None
    job_location: Optional[str] = None
    job_skills: Optional[List[str]] = None
    job_type: Optional[Literal["Full-time", "Part-time", "Contract"]] = None
    job_salary: Optional[int] = None
    job_requirements: Optional[List[str]] = None
    job_posted_date: Optional[date] = None
    posted_by_name: Optional[str] = None
    posted_by_mobile: Optional[str] = None

    class Config:
        extra = "forbid"

# job delete model
class jobDelete(BaseModel):
    job_id: str

    class Config:
        extra = "forbid"

# job search model
class jobSearch(BaseModel):
    job_title: str
    class Config:
        extra = "forbid"


