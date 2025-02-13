from views.view import View
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from helpers.helpers import Items, ViewState

class ProfileView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.PROFILE
        self.theWindow = uic.loadUi("qtdesigner/profile_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png")) 

        self.theItemMap = {
            Items.HOME       : self.theWindow.findChild(QPushButton, "btnHome"),
            Items.SETTINGS   : self.theWindow.findChild(QPushButton, "btnSettings"),
            Items.PROFILE    : self.theWindow.findChild(QPushButton, "btnProfile"),
            Items.STATS      : self.theWindow.findChild(QPushButton, "btnStats")
        }


    # Update from Controller, updating button UI elements
    def updateItemUI(self, aSignal: Signal) -> None:
        if aSignal.theItem in self.theItemMap:
            self.theItemMap[aSignal.theItem].setChecked(aSignal.theState)
            self.theItemMap[aSignal.theItem].setText(aSignal.theText)
            self.theNavSignal.emit(aSignal)

            # DEBUG STATEMENT
            print(f"Updated {aSignal.theItem}: {aSignal.theText} (State: {aSignal.theState})")


