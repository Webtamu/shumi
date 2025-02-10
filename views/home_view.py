from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from views.view import View
from helpers.signals import Signal

class HomeView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theWindow = uic.loadUi("qtdesigner/home_design.ui")
        self.theWindow.setWindowIcon(QIcon("resources/orange_puffle.png"))

        print("HomeView Initialized") #DEBUG

        self.theButtonMap = {
            "btnStart": self.theWindow.findChild(QPushButton, "btnStart"),
            "btnSettings": self.theWindow.findChild(QPushButton, "btnSettings"),
            "btnProfile": self.theWindow.findChild(QPushButton, "btnProfile"),
            "btnStats": self.theWindow.findChild(QPushButton, "btnStats"),
        }

    # Update from Controller, updating button UI elements
    def doUpdateButtonUI(self, aSignal: Signal) -> None:
        if aSignal.theItemName in self.theButtonMap:
            self.theButtonMap[aSignal.theItemName].setChecked(aSignal.theState)
            self.theButtonMap[aSignal.theItemName].setText(aSignal.theText)
            self.theNavSignal.emit(aSignal)

            # DEBUG STATEMENT
            print(f"Updated {aSignal.theItemName}: {aSignal.theText} (State: {aSignal.theState})")
    

