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
            "pushButton": self.theWindow.findChild(QPushButton, "pushButton"),
            "pushButton_2": self.theWindow.findChild(QPushButton, "pushButton_2"),
            "pushButton_3": self.theWindow.findChild(QPushButton, "pushButton_3"),
            "pushButton_4": self.theWindow.findChild(QPushButton, "pushButton_4"),
        }
    # Response from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)

            self.theNavSignal.emit(aButtonName)

            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (State: {aState})")


