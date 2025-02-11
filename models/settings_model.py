from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, Actions

class SettingsModel(Model):
    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theItemStateData = {
            Items.HOME       : {"state": False, "text": "Return Home"},
            Items.SETTINGS   : {"state": False, "text": "Settings"},
            Items.PROFILE    : {"state": False, "text": "Profile"},
            Items.STATS      : {"state": False, "text": "Stats"},
            Items.REPORT_BUG : {"state": False, "text": "Report a Bug"},
            Items.CONTACT    : {"state": False, "text": "Contact Us"},
            Items.ABOUT      : {"state": False, "text": "About"},
        }

    # Update data store and notify controller
    def updateItemState(self, anItem: Items) -> None:
        if anItem in self._theItemStateData:
            theItem = self._theItemStateData[anItem]
            theItem["state"] = not theItem["state"]
            theText = theItem.get("alt", theItem["text"]) if theItem["state"] else theItem["text"]
            self.theModelSignal.emit(Signal(theActionType=Actions.BTN_PRESS, 
                                             theItem=anItem, 
                                             theState=theItem["state"], 
                                             theText=theText)
                                      )
            
