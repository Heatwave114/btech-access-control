import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Database:
    callback_done = threading.Event()
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
        doc_ref = self.db.collection(u'access').document(u'control')
        # self._control = doc_ref.get().to_dict()
        def on_snapshot(doc_snapshot, changes, read_time):
            self._control = doc_ref.get().to_dict()
            print('--------------control_changed-------------------')
        doc_watch = doc_ref.on_snapshot(on_snapshot)
        # print('control----------', self._control)

    def get_door(self):
        doc_ref = self.db.collection(u'access').document(u'door')
        # self._door = doc_ref.get().to_dict()
        def on_snapshot(doc_snapshot, changes, read_time):
            self._door = doc_ref.get().to_dict()
            print('--------------door_changed-------------------')
        doc_watch = doc_ref.on_snapshot(on_snapshot)
        # print('door----------', self._door)

    def return_access_list(self):
        return self._access_list

    def return_control(self):
        return self._control

    def return_door(self):
        return self._door

    def write_to_logs(self, log):
        log_ref = self.db.collection(u'logs').document(log['time'])
        log.pop("time")
        log_ref.set(log)

# database = Database()
# _access_list = database.return_access_list()
# _control = database.return_control()
# _door = database.return_door()
# print('access----------', _access_list)
# print('control---------', _control)
# print('door------------', _door)
# # get_access_list()
# # get_control()
# # get_door()
