from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal
from abc import abstractmethod

from helpers.helpers import Items
from helpers.signals import Signal

class Model(QObject):

    theModelSignal = pyqtSignal(Signal)

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.theDataMap = {}
        self.theActionMap = {}
        self.theModelType = None

    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self.theDataMap)

    # Update data store and notify controller
    @abstractmethod
    def updateModel(self, aSignal: Signal) -> None:
        ...
