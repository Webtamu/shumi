from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items
from helpers.logger import Logger

class ApplicationModel(Model):
    '''
    This class houses temporary application metadata which will be cleared on app reload.
    '''

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {
            Items.HOME       : {"state": False, "text": "Return Home", "nav": True},
            Items.SETTINGS   : {"state": False, "text": "Settings", "nav": True},
            Items.PROFILE    : {"state": False, "text": "Profile", "nav": True},
            Items.STATS      : {"state": False, "text": "Stats", "nav": True},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug", "nav": False},
            Items.CONTACT    : {"state": False, "text": "Contact Us", "nav": False},
            Items.ABOUT      : {"state": False, "text": "About", "nav": False},
            Items.BEGIN_TAKE : {"state": False, "text": "Begin Take", "nav": True},
            Items.LOGIN_CREATE_ACCOUNT  : {"state": False, "text": "Create account", "nav": True},
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT : {"state": False, "text": "Already have an account? Sign in", "nav": True},
        }

        self.theActionMap = {
         
        }

        self.theThread = None 
        self.theModelType = "Application"
    
    # Update data store and notify controller
    def updateModel(self, aSignal: Signal) -> None:

        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction()

        theItemEntry = self.theDataMap[aSignal.theItem]

        theItemEntry["state"] = not theItemEntry["state"]
        aSignal.theText = theItemEntry["text"]
        aSignal.theState = theItemEntry["state"]
        aSignal.theNavTag = theItemEntry["nav"]

        if aSignal.theDebugTag:
            Logger.info(f'{self.theModelType} Model Handled: {aSignal}')
        
        self.theModelSignal.emit(aSignal)

  
    
            
