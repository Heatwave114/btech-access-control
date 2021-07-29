import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Database:
    def __init__(self):
        cred = credentials.Certificate("../btech-69920-firebase-adminsdk-zxrjx-1ccf20dca3.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.get_access_list()
        self.get_control()
        self.get_door()

    def get_access_list(self):
        self._access_list = {}
        _access_list_no_id = self.db.collection(u'list')
        docs = _access_list_no_id.stream()
        for doc in docs:
            self._access_list.update({doc.id: doc.to_dict()})
        print(self._access_list)

    def get_control(self):
        self._control = self.db.collection(u'access').document(u'control').get()
        print(self._control)

    def get_door(self):
        self._door = self.db.collection(u'access').document(u'door').get()
        print(self._door)

    def return_access_list(self):
        return self._access_list

    def return_control(self):
        return self._control

    def return_door(self):
        return self._door

# database = Database()
# _access_list = database.return_access_list()
# _control = database.return_control()
# _door = database.return_door()
# print('access----------', _access_list)
# print('control---------', _control)
# print('door------------', _door)
# get_access_list()
# get_control()
# get_door()