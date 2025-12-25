from data_models import TotalCrop
import firebase_admin
from firebase_admin import credentials, firestore
from data_models import Farmer , Crop
from fastapi import FastAPI, HTTPException

app = FastAPI()
cred = credentials.Certificate("farmez-7d8a9-firebase-adminsdk-fbsvc-fa0a8d8674.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.post("/create-basic-farmer")
async def create_farmer(farmer: Farmer):
    try:
        # We use the Mobile Number as the Document ID. 
        # This prevents duplicate entries for the same person.
        doc_ref = db.collection('farmers').document(farmer.mobile_number)
        
        # Check if farmer already exists
        if doc_ref.get().exists:
            raise HTTPException(status_code=400, detail="Farmer with this mobile number already exists.")

        # Convert the Pydantic model to a Python Dictionary (JSON-like)
        farmer_data = farmer.dict()
        
        # Save to Firestore
        doc_ref.set(farmer_data)
        
        return {"status": "success", "message": f"Farmer {farmer.name} profile created successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-basic-farmer/{mobile_number}")
async def get_farmer(mobile_number: str):
    doc_ref = db.collection('farmers').document(mobile_number)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Farmer not found")


@app.post("/create-crop")
async def create_crop(mobile_number: str, crop: Crop): 
    try:
        doc_ref = db.collection('farmers').document(mobile_number)
        
        # Check if farmer exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        # 2. Convert the single crop object to a dict
        crop_data = crop.dict()
        
        # 3. Add to Firestore
        # ArrayUnion appends this new dictionary to the existing 'crops' list
        doc_ref.update({"crops": firestore.ArrayUnion([crop_data])})
        
        return {"status": "success", "message": "Crop added successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))