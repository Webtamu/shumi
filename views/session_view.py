from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel

from views.view import View
from helpers.helpers import Items, Actions, ViewState

class SessionView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.SESSION
        self.theWindow = uic.loadUi("qtdesigner/session_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.STOP  : { "instance": self.theWindow.findChild(QPushButton, "btnStop"), "action": Actions.BTN_PRESS },
            Items.TIMER : { "instance": self.theWindow.findChild(QLabel, "lblTimer"),     "action": Actions.NONE },
        }
