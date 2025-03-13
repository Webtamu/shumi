from PyQt6.QtCore import pyqtSignal

from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, Colors
from utils.timer import Timer

USER_DEFINED_TIME_PERIOD = 10

class ApplicationModel(Model):
    '''
    This class houses temporary application metadata which will be cleared on app reload.
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {
            Items.HOME       : {"state": False, "text": "Return Home"},
            Items.START      : {"state": False, "text": "Start Session"},
            Items.STOP       : {"state": False, "text": "Stop Session"},
            Items.SETTINGS   : {"state": False, "text": "Settings"},
            Items.PROFILE    : {"state": False, "text": "Profile"},
            Items.STATS      : {"state": False, "text": "Stats"},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug"},
            Items.CONTACT    : {"state": False, "text": "Contact Us"},
            Items.ABOUT      : {"state": False, "text": "About"},
            Items.TIMER      : {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
        }

        self.theActionMap = {
            Items.START : self.beginTimer,
            Items.STOP  : self.stopTimer,
        }

        self.theThread = None 
    
    def beginTimer(self) -> None:
        self.theThread = Timer(USER_DEFINED_TIME_PERIOD)
        self.theThread.theTimerSignal.connect(self.updateItemState)
        self.theThread.start()
    
    def stopTimer(self) -> None:
        if self.theThread:
            self.theThread.stop()
            self.theThread = None
            

            
