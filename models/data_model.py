import json
import duckdb

from services.supabase_service import SupabaseService
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, Colors

class DataModel(Model):
    '''
    This class houses table data, which is local storage that can be synced to cloud.
    '''

    def __init__(self) -> None:
        super().__init__()
        
        self.theDatabase = SupabaseService()

        self.theDataMap = {
            Items.SYNC       : {"state": False, "text": "Sync"},
            Items.LOGIN      : {"state": False, "text": "Login"},
        }

        self.theActionMap = {
            Items.SYNC: self.syncToCloud,
            Items.LOGIN: self.login,
        }
        
        self.theModelType = "Data"
        self.theUserID = None

    def syncToCloud(self, aSignal: Signal) -> None:
        theResponse = self.theDatabase.fetchData(aTableName='DuckDB')
        print(json.dumps(theResponse.data, indent=4))

        self.theDatabase.logout()

        theResponse = self.theDatabase.fetchData(aTableName='DuckDB')
        print(theResponse.data)
    
    def login(self, aSignal: Signal) -> None:

        theUsername = aSignal.theData.get("username")  
        thePassword = aSignal.theData.get("password")

        self.theDatabase.login(anEmail=theUsername, aPassword=thePassword)

        if self.theDatabase.isConnected():
            print("Successfully connected to Supabase.")
            theUserInfo = self.theDatabase.getUserInfo()
            self.theUserID = theUserInfo.user.id

    def updateModel(self, aSignal: Signal) -> None:
        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction(aSignal)

        theItemEntry = self.theDataMap[aSignal.theItem]
        theItemEntry["state"] = not theItemEntry["state"]

        aSignal.theText = theItemEntry["text"]
        aSignal.theState = theItemEntry["state"]
   
        if aSignal.theDebugTag:
            print(f"{Colors.CYAN}{self.theModelType} Model Handled:{Colors.RESET}", aSignal)

        self.theModelSignal.emit(aSignal)