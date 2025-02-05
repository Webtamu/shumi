from PyQt6.QtCore import pyqtSignal
from models.models import Model

class SettingsModel(Model):
    # Signal that carries <btnName, state, text>
    theButtonSignal = pyqtSignal(str, bool, str)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theButtonStateData = {
            "btnStart": {"state": False, "text": "Start Session", "alt": "Stop Session"},
            "btnSettings": {"state": False, "text": "Settings"},
            "btnProfile": {"state": False, "text": "Profile"},
            "btnStats": {"state": False, "text": "Stats"},
        }
    
    # Update data store and notify controller
    def doUpdateButtonState(self, aButtonName: str) -> None:
        if aButtonName in self._theButtonStateData:
            theButton = self._theButtonStateData[aButtonName]
            theButton["state"] = not theButton["state"]

            theText = theButton.get("alt", theButton["text"]) if theButton["state"] else theButton["text"]
            self.theButtonSignal.emit(aButtonName, theButton["state"], theText)
            
