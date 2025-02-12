from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from views.view import View
from helpers.signals import Signal
from helpers.helpers import Items, ViewState

class HomeView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.HOME
        self.theWindow = uic.loadUi("qtdesigner/home_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png"))

        self.theItemMap = {
            Items.START    : self.theWindow.findChild(QPushButton, "btnStart"),
            Items.SETTINGS : self.theWindow.findChild(QPushButton, "btnSettings"),
            Items.PROFILE  : self.theWindow.findChild(QPushButton, "btnProfile"),
            Items.STATS    : self.theWindow.findChild(QPushButton, "btnStats"),
        }
        
    # Update from Controller, updating button UI elements
    def updateItemUI(self, aSignal: Signal) -> None:
        if aSignal.theItem in self.theItemMap:
            self.theItemMap[aSignal.theItem].setChecked(aSignal.theState)
            self.theItemMap[aSignal.theItem].setText(aSignal.theText)
            self.theNavSignal.emit(aSignal)

            # DEBUG STATEMENT
            print(f"Updated {aSignal.theItem}: {aSignal.theText} (State: {aSignal.theState})")
    

