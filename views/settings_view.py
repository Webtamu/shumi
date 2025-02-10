from views.view import View
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal

class SettingsView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theWindow = uic.loadUi("qtdesigner/settings_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png")) 

        self.theButtonMap = {
            "btnHome": self.theWindow.findChild(QPushButton, "btnHome"),
            "btnSettings": self.theWindow.findChild(QPushButton, "btnSettings"),
            "btnProfile": self.theWindow.findChild(QPushButton, "btnProfile"),
            "btnBug": self.theWindow.findChild(QPushButton, "btnBug"),
            "btnContact": self.theWindow.findChild(QPushButton, "btnContact"),
            "btnAbout": self.theWindow.findChild(QPushButton, "btnAbout"),
        }

    # Update from Controller, updating button UI elements
    def doUpdateButtonUI(self, aSignal: Signal) -> None:
        if aSignal.theItemName in self.theButtonMap:
            self.theButtonMap[aSignal.theItemName].setChecked(aSignal.theState)
            self.theButtonMap[aSignal.theItemName].setText(aSignal.theText)
            self.theNavSignal.emit(aSignal)

            # DEBUG STATEMENT
            print(f"Updated {aSignal.theItemName}: {aSignal.theText} (State: {aSignal.theState})")


