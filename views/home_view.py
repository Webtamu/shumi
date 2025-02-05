from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic

from ui.streak import Placeholder
from views.view import View

class HomeView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theWindow = uic.loadUi("qtdesigner/home_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png")) 
        self.theButtonMap = {
            "btnStart": self.theWindow.findChild(QPushButton, "btnStart"),
            "btnSettings": self.theWindow.findChild(QPushButton, "btnSettings"),
            "btnProfile": self.theWindow.findChild(QPushButton, "btnProfile"),
            "btnStats": self.theWindow.findChild(QPushButton, "btnStats"),
        }

    # Update from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)
            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (State: {aState})")
