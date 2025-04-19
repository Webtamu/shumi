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
            Items.LOGIN_LOGIN : {"state": False, "text": "Login"},
            Items.START      : {"state": False, "text": "Start Session"},
            Items.STOP       : {"state": False, "text": "Stop Session"},
            Items.TIMER      : {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
        }

        self.theActionMap = {
            Items.SYNC: self.syncToCloud,
            Items.LOGIN_LOGIN : self.login,
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

        # TODO: Auto-login
        self.theDatabase.login(anEmail="testuser@gmail.com", aPassword="testpass")
        #self.theDatabase.login(anEmail=theUsername, aPassword=thePassword)

        if self.theDatabase.isConnected():
            theUserInfo = self.theDatabase.getUserInfo()
            self.theUserID = theUserInfo.user.id
            aSignal.theNavTag = True

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
        aSignal.theNavTag = True
        self.theThread = Timer(USER_DEFINED_TIME_PERIOD)
        self.theThread.theTimerSignal.connect(self.updateModel)
        self.theThread.start()
    
    def stopTimer(self, aSignal: Signal) -> None:
        aSignal.theNavTag = True
        if self.theThread:
            self.theThread.stop()
            self.addSession(self.theUserID, self.theThread.theStartTime, self.theThread.theStopTime)
            self.theThread = None

    def syncToCloudTest(self) -> None:
        """Sync local DuckDB unsynced sessions to Supabase and mark them as synced."""
        unsynced_sessions = self.theLocalDatabase.collect_unsynced()

        if not unsynced_sessions:
            print(f"{Colors.YELLOW}No unsynced sessions to upload.{Colors.RESET}")
            return

        synced_ids = self.theDatabase.upload_unsynced_sessions(unsynced_sessions)

        if synced_ids:
            self.theLocalDatabase.mark_as_synced(synced_ids)
            print(f"{Colors.GREEN}Synced {len(synced_ids)} session(s) to Supabase.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Failed to sync any sessions.{Colors.RESET}")

            
        
            
