from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from models.models import Model
from helpers.helpers import Items, Actions, ViewState

class PreferencesModel(Model):
    '''
    This class houses user preferences data, which needs to be saved and reloaded on app reload
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self._thePreferencesData = {}
    
    # Update data store and notify controller
    def updateItemState(self, anItem: Items, aViewState: ViewState) -> None:
        if anItem in self._theTempStateData:
            theItem = self._theTempStateData[anItem]
            theItem["state"] = not theItem["state"]
            theText = theItem.get("alt", theItem["text"]) if theItem["state"] else theItem["text"]
            self.theModelSignal.emit(Signal(theActionType=Actions.BTN_PRESS, 
                                             theItem=anItem, 
                                             theState=theItem["state"], 
                                             theText=theText,
                                             theSource=aViewState)
                                      )
            
