from PyQt6.QtCore import QObject, pyqtSignal

class Model(QObject):
    # Signal that carries <btnName, state, text>
    theButtonSignal = pyqtSignal(str, bool, str)  
    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theButtonStateData = {
            "btnStart": {"state": False, "text": "Start Session", "offText": "Start Session", "onText": "Stop Session"},
            "btnSettings": {"state": False, "text": "Settings", "offText": "Settings", "onText": "Close Settings"},
            "btnProfile": {"state": False, "text": "Profile", "offText": "Profile", "onText": "Close Profile"},
        }
    
    # Update data store and notify controller
    def doUpdateButtonState(self, aButtonName: str) -> None:
        if aButtonName in self._theButtonStateData:
            theButton = self._theButtonStateData[aButtonName]
            theButton["state"] = not theButton["state"]
            theButton["text"] = theButton["onText"] if theButton["state"] else theButton["offText"]
            self.theButtonSignal.emit(aButtonName, self._theButtonStateData[aButtonName]["state"], self._theButtonStateData[aButtonName]["text"])
