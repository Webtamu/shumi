from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, Colors


class ApplicationModel(Model):
    '''
    This class houses temporary application metadata which will be cleared on app reload.
    '''

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {
            Items.HOME       : {"state": False, "text": "Return Home"},
            Items.SETTINGS   : {"state": False, "text": "Settings"},
            Items.PROFILE    : {"state": False, "text": "Profile"},
            Items.STATS      : {"state": False, "text": "Stats"},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug"},
            Items.CONTACT    : {"state": False, "text": "Contact Us"},
            Items.ABOUT      : {"state": False, "text": "About"},
            Items.BEGIN_TAKE : {"state": False, "text": "Begin Take"},
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
        aSignal.theNavTag = True

        if aSignal.theDebugTag:
            print(f"{Colors.CYAN}{self.theModelType} Model Handled:{Colors.RESET}", aSignal)
        
        self.theModelSignal.emit(aSignal)

  
    
            
