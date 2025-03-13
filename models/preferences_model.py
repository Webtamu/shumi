from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, Colors, ViewState

class PreferencesModel(Model):
    '''
    This class houses user preferences data, which needs to be saved and reloaded on app reload
    '''

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {
            Items.DARK_MODE : { "state" : False, "text": "Dark Mode"},
            Items.LANGUAGE  : { "state" : False, "text": "Language" },
            Items.TIME      : { "state" : False, "text": "Time" }
        }

        self.theActionMap = {}
        self.theModelType = "Preferences"

    def __del__(self):
        print("Writing preferences data to json!")

    # Update data store and notify controller
    def updateModel(self, aSignal: Signal) -> None:
        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction()

        theItemEntry = self.theDataMap[aSignal.theItem]
        theItemEntry["state"] = not theItemEntry["state"]

        aSignal.theText = theItemEntry["text"]
        aSignal.theState = theItemEntry["state"]
        aSignal.theSource = ViewState.ALL

        if aSignal.theDebugTag:
            print(f"{Colors.CYAN}{self.theModelType} Model Handled:{Colors.RESET}", aSignal)

        self.theModelSignal.emit(aSignal)


