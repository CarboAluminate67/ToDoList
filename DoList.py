import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('C:\Users\alext\OneDrive\Documents\BYUI\Junior\cse310\"Sprint 6"\todolist-8f647-c6da598b8c29.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
