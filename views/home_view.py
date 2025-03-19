from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton

from views.view import View
from helpers.helpers import Items, Actions, ViewState

class HomeView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.HOME
        self.theWindow = uic.loadUi("qtdesigner/home_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.START    : { "instance": self.theWindow.findChild(QPushButton, "btnStart"),    "action": Actions.BTN_PRESS },
            Items.SETTINGS : { "instance": self.theWindow.findChild(QPushButton, "btnSettings"), "action": Actions.BTN_PRESS },
            Items.PROFILE  : { "instance": self.theWindow.findChild(QPushButton, "btnProfile"),  "action": Actions.BTN_PRESS },
            Items.STATS    : { "instance": self.theWindow.findChild(QPushButton, "btnStats"),    "action": Actions.BTN_PRESS },
        }
 
            
         