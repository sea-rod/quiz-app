import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def firebase_connect():
    # cred = credentials.Certificate('./fire_auth/quiz-cc089-firebase-adminsdk-fbsvc-9efb4af903.json')
    firebase_admin.initialize_app()
    return firestore.client()
