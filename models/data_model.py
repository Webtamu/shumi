from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, Actions, ViewState

class DataModel(Model):
    '''
    This class houses table data, which is local storage that can be synced to cloud.
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._theTableData = {}
    

    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self._theTableData)

    # Update data store and notify controller
    def updateItemState(self, aSignal: Signal) -> None:
        if aSignal.theDebugTag:
            print("DATA MODEL HANDLING!!")
        theItemEntry = self._theTableData[aSignal.theItem]
        theItemEntry["state"] = not theItemEntry["state"]
        aSignal.theState = theItemEntry["state"]
        self.theModelSignal.emit(aSignal)
