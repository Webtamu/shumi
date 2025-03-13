from PyQt6.QtCore import pyqtSignal

from models.models import Model
from helpers.signals import Signal

class DataModel(Model):
    '''
    This class houses table data, which is local storage that can be synced to cloud.
    '''

    theModelSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.theDataMap = {}
        self.theActionMap = {}


