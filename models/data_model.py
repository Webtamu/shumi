import json

from services.duckdb_service import DuckDBService
from services.supabase_service import SupabaseService
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items
from helpers.logger import Logger
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
            Items.CREATE_ACCOUNT_CREATE : {"state": False, "text": "Create Account"},
        }

        self.theActionMap = {
            Items.SYNC: self.syncToCloud,
            Items.LOGIN_LOGIN : self.login,
            Items.START : self.beginTimer,
            Items.STOP  : self.stopTimer,
            Items.CREATE_ACCOUNT_CREATE : self.createAccount,
        }
        
        self.theModelType = "Data"
        self.theUserID: str = None
    
    def syncToCloud(self, aSignal: Signal) -> None:
        # Check if logged in
        Logger.debug(self.theLocalDatabase.fetch_data('session'))


        theUnsyncedRows = self.theLocalDatabase.collect_unsynced()
        syncedRows = self.theDatabase.upload_unsynced_sessions(theUnsyncedRows)
        self.theLocalDatabase.mark_as_synced(syncedRows)

        Logger.debug(self.theLocalDatabase.fetch_data('session'))

    def createAccount(self, aSignal: Signal) -> None:
        theUsername = aSignal.theData.get("user")
        theEmail = aSignal.theData.get("email")
        thePassword = aSignal.theData.get("pass")
        thePasswordConfirm = aSignal.theData.get("confirm_pass")
        
        if not theUsername or not theEmail or not thePassword:
            Logger.error("Account creation failed: Missing required fields")
            return
        
        if thePassword != thePasswordConfirm:
            Logger.error("Account creation failed: Passwords do not match")
            return
        
        if "@" not in theEmail or "." not in theEmail:
            Logger.error("Account creation failed: Invalid email format")
            return
        
        self.theDatabase.createAccount(theEmail, thePassword, theUsername)

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
            Logger.info(f'{self.theModelType} Model Handled: {aSignal}')
        

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
            Logger.info(f'No unsynced sessions to upload.')
            return

        synced_ids = self.theDatabase.upload_unsynced_sessions(unsynced_sessions)

        if synced_ids:
            self.theLocalDatabase.mark_as_synced(synced_ids)
            Logger.info(f'Synced {len(synced_ids)} session(s) to Supabase.')
        else:
            Logger.error(f"Failed to sync any sessions.")

            
        
            
