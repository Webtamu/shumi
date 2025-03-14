import json
from pprint import pprint

from services.supabase_service import SupabaseService
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items

class DataModel(Model):
    '''
    This class houses table data, which is local storage that can be synced to cloud.
    '''

    def __init__(self) -> None:
        super().__init__()
        
        self.theDatabase = SupabaseService()

        self.theDatabase.login(anEmail="testuser@gmail.com", aPassword="testpass")

        if self.theDatabase.isConnected():
            print("Successfully connected to Supabase.")

        self.theDataMap = {
            Items.SYNC       : {"state": False, "text": "Sync"},
        }

        self.theActionMap = {
            Items.SYNC: self.syncToCloud,
        }

        self.theModelType = "Data"

    def syncToCloud(self, aSignal: Signal) -> None:
        theResponse = self.theDatabase.fetchData(aTableName='users')
        print(json.dumps(theResponse.data, indent=4))


        self.theDatabase.logout()

        theResponse = self.theDatabase.fetchData(aTableName='users')
        print(theResponse.data)

    def updateModel(self, aSignal: Signal) -> None:
        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction(aSignal)
    