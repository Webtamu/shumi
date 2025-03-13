from PyQt6.QtCore import pyqtSignal

from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items

class PreferencesModel(Model):
    '''
    This class houses user preferences data, which needs to be saved and reloaded on app reload
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {
            Items.DARK_MODE : { "state" : False, "text": "Dark Mode"},
            Items.LANGUAGE  : { "state" : False, "text": "Language" },
            Items.TIME      : { "state" : False, "text": "Time" }
        }

        self.theActionMap = {}

    def __del__(self):
        print("Writing preferences data to json!")


