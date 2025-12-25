import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("farmez-7d8a9-firebase-adminsdk-fbsvc-fa0a8d8674.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# Define the data for your simple document
data = {
    "name": "First Document",
    "description": "This is a simple document in a new collection."
}

# Add a document to a collection named 'my_new_collection'
# If the collection 'my_new_collection' doesn't exist, it will be created.
# .add() automatically generates a document ID.
doc_id = "praba_1"
doc_ref = db.collection("my_new_collection").document(doc_id)

doc_ref.update({"name": firestore.DELETE_FIELD,
"my_name": "sanjay"})
print(f"Document updated with ID: {doc_ref}")