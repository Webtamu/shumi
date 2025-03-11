from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, Actions, ViewState
from utils.timer import Timer

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
            Items.START      : {"state": False, "text": "Start Session"},
            Items.STOP       : {"state": False, "text": "Stop Session"},
            Items.SETTINGS   : {"state": False, "text": "Settings"},
            Items.PROFILE    : {"state": False, "text": "Profile"},
            Items.STATS      : {"state": False, "text": "Stats"},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug"},
            Items.CONTACT    : {"state": False, "text": "Contact Us"},
            Items.ABOUT      : {"state": False, "text": "About"},
            Items.TIMER      : {"state": False, "text": "10"},
        }
    
    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self._theTempStateData)
    
    def beginTimer(self):
        self.theThread = Timer(10)
        self.theThread.theTimerSignal.connect(self.updateItemState)
        self.theThread.start()

    # Update data store and notify controller
    def updateItemState(self, aSignal: Signal) -> None:
        if aSignal.theItem == Items.START:
            self.beginTimer()

        if aSignal.theDebugTag:
            print("App Model Handling:", aSignal)

        theItemEntry = self._theTempStateData[aSignal.theItem]

        if aSignal.theItem != Items.TIMER:  # Don't overwrite dynamic text (like timer)
            theItemEntry["state"] = not theItemEntry["state"]
            aSignal.theState = theItemEntry["state"]
            aSignal.theText = theItemEntry["text"]
        else:
            aSignal.theState = theItemEntry["state"]

        self.theModelSignal.emit(aSignal)
            

            
