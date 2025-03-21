import json

from services.duckdb_service import DuckDBService
from services.supabase_service import SupabaseService
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, Colors
from utils.timer import Timer

USER_DEFINED_TIME_PERIOD = 10

class DataModel(Model):
    '''
    This class houses table data, which is local storage that can be synced to cloud.
    '''

    def __init__(self) -> None:
        super().__init__()
        
        self.theDatabase = SupabaseService()
        self.theLocalDatabase = DuckDBService()

        self.theDataMap = {
            Items.SYNC       : {"state": False, "text": "Sync"},
            Items.LOGIN      : {"state": False, "text": "Login"},
            Items.START      : {"state": False, "text": "Start Session"},
            Items.STOP       : {"state": False, "text": "Stop Session"},
            Items.TIMER      : {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
        }

        self.theActionMap = {
            Items.SYNC: self.syncToCloud,
            Items.LOGIN: self.login,
            Items.START : self.beginTimer,
            Items.STOP  : self.stopTimer,
        }
        
        self.theModelType = "Data"
        self.theUserID: str = None

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
            self.theUserID = str(theUserInfo.user.id)

    def updateModel(self, aSignal: Signal) -> None:
        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction(aSignal)

        theItemEntry = self.theDataMap[aSignal.theItem]
        if aSignal.theItem != Items.TIMER:  # Don't overwrite dynamic text (like timer)
            theItemEntry["state"] = not theItemEntry["state"]
            aSignal.theText = theItemEntry["text"]
            aSignal.theState = theItemEntry["state"]
   
        if aSignal.theDebugTag:
            print(f"{Colors.CYAN}{self.theModelType} Model Handled:{Colors.RESET}", aSignal)

        self.theModelSignal.emit(aSignal)


    def addSession(self, aUserID, aStartTime, aStopTime) -> None:
        # Get session info from supabase session

        self.theLocalDatabase.insert_data(aUserID, aStartTime, aStopTime)

        return

    def beginTimer(self, aSignal: Signal) -> None:
        self.theThread = Timer(USER_DEFINED_TIME_PERIOD)
        self.theThread.theTimerSignal.connect(self.updateModel)
        self.theThread.start()
    
    def stopTimer(self, aSignal: Signal) -> None:
        if self.theThread:
            self.theThread.stop()
            self.addSession(self.theUserID, self.theThread.theStartTime, self.theThread.theStopTime)
            self.theThread = None

            
        
            
