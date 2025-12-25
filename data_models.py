from pydantic import BaseModel
from typing import Optional , Literal , List
from datetime import date

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
    