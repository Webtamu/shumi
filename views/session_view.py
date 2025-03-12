from views.view import View
from PyQt6.QtWidgets import QPushButton, QLabel
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
            Items.STOP  : self.theWindow.findChild(QPushButton, "btnStop"),
            Items.TIMER : self.theWindow.findChild(QLabel, "lblTimer"),
        }
        
     