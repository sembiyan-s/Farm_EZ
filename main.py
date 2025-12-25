from data_models import TotalCrop
import firebase_admin
from firebase_admin import credentials, firestore
from data_models import Farmer , Crop , FarmerUpdate , LabourProfile , LabourProfileUpdate , Job , JobUpdate , JobCreate
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

app = FastAPI()
cred = credentials.Certificate("farmez-7d8a9-firebase-adminsdk-fbsvc-fa0a8d8674.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# farmer related API 
# create  farmer profile
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

# get farmer profile
@app.get("/get-basic-farmer/{mobile_number}")
async def get_farmer(mobile_number: str):
    doc_ref = db.collection('farmers').document(mobile_number)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Farmer not found")

# update farmer profile
@app.patch("/update-basic-farmer/{mobile_number}")
async def update_farmer(mobile_number: str, farmer_update: FarmerUpdate):
    try:
        doc_ref = db.collection('farmers').document(mobile_number)
        
        # Check if farmer exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        # Filter out None values to only update provided fields
        update_data = farmer_update.dict(exclude_unset=True)
        
        if not update_data:
             raise HTTPException(status_code=400, detail="No fields provided for update")

        # Update Firestore
        doc_ref.update(update_data)
        
        return {"status": "success", "message": f"Farmer profile updated successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# delete farmer profile
@app.delete("/delete-basic-farmer/{mobile_number}")
async def delete_farmer(mobile_number: str):
    try:
        doc_ref = db.collection('farmers').document(mobile_number)
        
        # Check if farmer exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        # Delete document
        doc_ref.delete()
        
        return {"status": "success", "message": "Farmer profile deleted successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# crop related API
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


# Labour related API
@app.post("/create-labour")
async def create_labour(labour: LabourProfile):
    try:
        doc_ref = db.collection('labours').document(labour.mobile_no)
        
        # Check if labour already exists
        if doc_ref.get().exists:
            raise HTTPException(status_code=400, detail="Labour with this mobile number already exists.")
        
        # Convert the Pydantic model to a Python Dictionary (JSON-like)
        labour_data = labour.dict()
        
        # Save to Firestore
        doc_ref.set(labour_data)
        
        return {"status": "success", "message": f"Labour {labour.name} profile created successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get labour profile
@app.get("/get-labour/{mobile_no}")
async def get_labour(mobile_no: str):
    doc_ref = db.collection('labours').document(mobile_no)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Labour not found")

# update labour profile
@app.patch("/update-labour/{mobile_no}")
async def update_labour(mobile_no: str, labour_update: LabourProfileUpdate):
    try:
        doc_ref = db.collection('labours').document(mobile_no)
        
        # Check if labour exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Labour not found")
        
        # Filter out None values to only update provided fields
        update_data = labour_update.dict(exclude_unset=True)
        
        if not update_data:
             raise HTTPException(status_code=400, detail="No fields provided for update")

        # Update Firestore
        doc_ref.update(update_data)
        
        return {"status": "success", "message": f"Labour profile updated successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# delete labour profile
@app.delete("/delete-labour/{mobile_no}")
async def delete_labour(mobile_no: str):
    try:
        doc_ref = db.collection('labours').document(mobile_no)
        
        # Check if labour exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Labour not found")
        
        # Delete document
        doc_ref.delete()
        
        return {"status": "success", "message": "Labour profile deleted successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

                        # job related API

# create job
@app.post("/create-job")
async def create_job(job: JobCreate):
    try:
        # Convert the Pydantic model to a Python Dictionary (JSON-like)
        # We use jsonable_encoder to handle types like datetime.date which Firestore doesn't accept directly
        job_data = jsonable_encoder(job)
        
        # Add to Firestore - add() generates a unique ID
        update_time, doc_ref = db.collection('jobs').add(job_data)
        
        # Get the generated ID
        new_job_id = doc_ref.id
        
        # Optionally update the document with its own ID if needed, or just return it
        # doc_ref.update({"job_id": new_job_id}) 
        # For this design, let's assume the ID is external to the data object in DB 
        # OR if we want to return a Job object which includes job_id as per our model:
        
        # Let's add the ID to the document too so it's self-contained when fetched
        doc_ref.update({"job_id": new_job_id})
        
        return {"status": "success", "message": f"Job {job.job_title} created successfully.", "job_id": new_job_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get job
@app.get("/get-job/{job_id}")
async def get_job(job_id: str):
    doc_ref = db.collection('jobs').document(job_id)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="Job not found")
        
# update job
@app.patch("/update-job/{job_id}")
async def update_job(job_id: str, job_update: JobUpdate):
    try:
        doc_ref = db.collection('jobs').document(job_id)
        
        # Check if job exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Filter out None values to only update provided fields
        update_data = job_update.dict(exclude_unset=True)
        # Convert to JSON compatible types (dates to strings) for Firestore
        update_data = jsonable_encoder(update_data)
        
        if not update_data:
             raise HTTPException(status_code=400, detail="No fields provided for update")

        # Update Firestore
        doc_ref.update(update_data)
        
        return {"status": "success", "message": f"Job updated successfully."}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# delete job
@app.delete("/delete-job/{job_id}")
async def delete_job(job_id: str):
    try:
        doc_ref = db.collection('jobs').document(job_id)
        
        # Check if job exists
        if not doc_ref.get().exists:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Delete document
        doc_ref.delete()
        
        return {"status": "success", "message": "Job deleted successfully."}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# search job
@app.get("/search-job/{job_title}")
async def search_job(job_title: str):
    doc_ref = db.collection('jobs').where('job_title', '==', job_title)
    docs = doc_ref.get()
    
    # docs is a list, so we check if it has any items
    if docs:
        return [doc.to_dict() for doc in docs]
    else:
        raise HTTPException(status_code=404, detail="Job not found")
