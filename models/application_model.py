from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, Actions, ViewState

class ApplicationModel(Model):
    '''
    This class houses temporary application metadata which will be cleared on app reload.
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theTempStateData = {
            Items.HOME       : {"state": False, "text": "Return Home"},
            Items.START      : {"state": False, "text": "Start Session", "alt": "Stop Session"},
            Items.SETTINGS   : {"state": False, "text": "Settings"},
            Items.PROFILE    : {"state": False, "text": "Profile"},
            Items.STATS      : {"state": False, "text": "Stats"},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug"},
            Items.CONTACT    : {"state": False, "text": "Contact Us"},
            Items.ABOUT      : {"state": False, "text": "About"},
        }
    
    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self._theTempStateData)
            
    # Update data store and notify controller
    def updateItemState(self, aSignal: Signal) -> None:
        print("APPLICATION MODEL HANDLING!!")
        theItemEntry = self._theTempStateData[aSignal.theItem]
        theItemEntry["state"] = not theItemEntry["state"]
        aSignal.theState = theItemEntry["state"]
        aSignal.theText = theItemEntry.get("alt", theItemEntry["text"]) if theItemEntry["state"] else theItemEntry["text"]
        self.theModelSignal.emit(aSignal)
            

            
