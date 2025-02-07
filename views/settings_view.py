from views.view import View
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal

class SettingsView(View):
    theNavSignal = pyqtSignal(str)

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

    # Response from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)
            self.theNavSignal.emit(aButtonName)
            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (State: {aState})")


