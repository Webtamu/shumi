from views.view import View
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from helpers.signals import Signal
from helpers.helpers import Items, ViewState

class StatsView(View):
    theNavSignal = pyqtSignal(Signal)

    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.STATS
        self.theWindow = uic.loadUi("qtdesigner/stats_design.ui")

        self.theItemMap = {
            Items.HOME       : self.theWindow.findChild(QPushButton, "btnHome"),
            Items.SETTINGS   : self.theWindow.findChild(QPushButton, "btnSettings"),
            Items.PROFILE    : self.theWindow.findChild(QPushButton, "btnProfile"),
        }

