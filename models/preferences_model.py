from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, ViewState

class PreferencesModel(Model):
    '''
    This class houses user preferences data, which needs to be saved and reloaded on app reload
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._thePreferencesData = {
            Items.DARK_MODE : { "state" : False },
            Items.LANGUAGE  : { "state" : False },
            Items.TIME      : { "state" : False }
        }

    def __del__(self):
        print("Writing preferences data to json!")

    
    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self._thePreferencesData)

    # Update data store and notify controller
    def updateItemState(self, aSignal: Signal) -> None:
        if aSignal.theDebugTag:
            print("PREFERENCES MODEL HANDLING!!")
        theItemEntry = self._thePreferencesData[aSignal.theItem]
        theItemEntry["state"] = not theItemEntry["state"]
        aSignal.theState = theItemEntry["state"]
        aSignal.theSource = ViewState.ALL
        self.theModelSignal.emit(aSignal)
            
