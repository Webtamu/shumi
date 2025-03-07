from views.view import View
from PyQt6.QtWidgets import QPushButton
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from helpers.helpers import Items, ViewState

class SessionView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.SESSION
        self.theWindow = uic.loadUi("qtdesigner/session_design.ui")

        self.theItemMap = {
            Items.STOP    : self.theWindow.findChild(QPushButton, "btnStop"),
        }
        
    # Update from Controller, updating button UI elements
    def updateItemUI(self, aSignal: Signal) -> None:
        if aSignal.theItem in self.theItemMap:
            self.theItemMap[aSignal.theItem].setChecked(aSignal.theState)
            self.theItemMap[aSignal.theItem].setText(aSignal.theText)
            self.theNavSignal.emit(aSignal) 
        if aSignal.theItem == Items.DARK_MODE:
            self.toggleDarkMode(aSignal)

        # DEBUG STATEMENT
        if aSignal.theDebugTag:
            print(f"Updated {aSignal.theItem}: {aSignal.theText} (State: {aSignal.theState})")    