from views.view import View
from PyQt6.QtWidgets import QPushButton, QCheckBox
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from helpers.helpers import Items, ViewState

class SettingsView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.SETTINGS
        self.theWindow = uic.loadUi("qtdesigner/settings_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png")) 

        self.theItemMap = {
            Items.HOME       : self.theWindow.findChild(QPushButton, "btnHome"),
            Items.SETTINGS   : self.theWindow.findChild(QPushButton, "btnSettings"),
            Items.PROFILE    : self.theWindow.findChild(QPushButton, "btnProfile"),
            Items.STATS      : self.theWindow.findChild(QPushButton, "btnStats"),
            Items.REPORT_BUG : self.theWindow.findChild(QPushButton, "btnBug"),
            Items.CONTACT    : self.theWindow.findChild(QPushButton, "btnContact"),
            Items.ABOUT      : self.theWindow.findChild(QPushButton, "btnAbout"),
            Items.DARK_MODE  : self.theWindow.findChild(QCheckBox, "boxDarkMode"),
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

