from PyQt6.QtCore import QObject
from abc import abstractmethod

from helpers.helpers import Items, Colors
from helpers.signals import Signal

class Model(QObject):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.theDataMap = {}
        self.theActionMap = {}
        self.theModelType = None

    def canHandle(self, aSignal: Signal) -> bool:
        return (aSignal.theItem in self.theDataMap)

    # Update data store and notify controller
    def updateItemState(self, aSignal: Signal) -> None:
        if theAction := self.theActionMap.get(aSignal.theItem):
            theAction()

        theItemEntry = self.theDataMap[aSignal.theItem]

        if aSignal.theItem != Items.TIMER:  # Don't overwrite dynamic text (like timer)
            theItemEntry["state"] = not theItemEntry["state"]
            aSignal.theText = theItemEntry["text"]
        aSignal.theState = theItemEntry["state"]

        if aSignal.theDebugTag:
            print(f"{Colors.CYAN}{self.theModelType} Model Handled:{Colors.RESET}", aSignal)

        self.theModelSignal.emit(aSignal)
