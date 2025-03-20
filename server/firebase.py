import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    cred = credentials.Certificate("../personai-dfb78-firebase-adminsdk-fbsvc-7ce7b2b7d7.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

def fetch_data_from_firebase(identity):
    db = initialize_firebase()
    doc_ref = db.collection("personas").document(identity)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        return "No such document!"