from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model

class SettingsModel(Model):
    # Signal that carries <btnName, state, text>
    theButtonSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theButtonStateData = {
            "btnHome": {"state": False, "text": "Return Home"},
            "btnSettings": {"state": False, "text": "Settings"},
            "btnProfile": {"state": False, "text": "Stats"},
            "btnBug": {"state": False, "text": "Report a Bug"},
            "btnContact": {"state": False, "text": "Contact Us"},
            "btnAbout": {"state": False, "text": "About"},
        }

    # Update data store and notify controller
    def doUpdateButtonState(self, aButtonName: str) -> None:
        if aButtonName in self._theButtonStateData:
            theButton = self._theButtonStateData[aButtonName]
            theButton["state"] = not theButton["state"]
            theText = theButton.get("alt", theButton["text"]) if theButton["state"] else theButton["text"]
            self.theButtonSignal.emit(Signal(anActionType="btnPress", 
                                             anItemName=aButtonName, 
                                             aState=theButton["state"], 
                                             aText=theText)
                                      )
            
