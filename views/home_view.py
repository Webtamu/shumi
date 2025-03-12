from PyQt6.QtWidgets import QPushButton
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

        self.theItemMap = {
            Items.START    : self.theWindow.findChild(QPushButton, "btnStart"),
            Items.SETTINGS : self.theWindow.findChild(QPushButton, "btnSettings"),
            Items.PROFILE  : self.theWindow.findChild(QPushButton, "btnProfile"),
            Items.STATS    : self.theWindow.findChild(QPushButton, "btnStats"),
        }
 
            
         