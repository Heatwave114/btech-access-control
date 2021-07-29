import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("../btech-69920-firebase-adminsdk-zxrjx-1ccf20dca3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

_access_list = {}
_control = {}
_door = {}

def get_access_list():
    global _access_list
    _access_list_no_id = db.collection(u'list')
    docs = _access_list_no_id.stream()
    for doc in docs:
        _access_list.update({doc.id: doc.to_dict()})
    print('access----------- ', _access_list)

def get_control():
    global _control
    _control = db.collection(u'access').document(u'control').get()
    print('control---------- ', _control)

def get_door():
    global _door
    _door = db.collection(u'access').document(u'door').get()
    print('door------------- ', _door)

get_access_list()
get_control()
get_door()