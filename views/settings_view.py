from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QCheckBox

from views.view import View
from helpers.helpers import Items, Actions, ViewState 

class SettingsView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.SETTINGS
        self.theWindow = uic.loadUi("qtdesigner/settings_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.HOME       : { "instance": self.theWindow.findChild(QPushButton, "btnHome"),     "action": Actions.BTN_PRESS },
            Items.SETTINGS   : { "instance": self.theWindow.findChild(QPushButton, "btnSettings"), "action": Actions.BTN_PRESS },
            Items.PROFILE    : { "instance": self.theWindow.findChild(QPushButton, "btnProfile"),  "action": Actions.BTN_PRESS },
            Items.STATS      : { "instance": self.theWindow.findChild(QPushButton, "btnStats"),    "action": Actions.BTN_PRESS },
            Items.REPORT_BUG : { "instance": self.theWindow.findChild(QPushButton, "btnBug"),      "action": Actions.BTN_PRESS },
            Items.CONTACT    : { "instance": self.theWindow.findChild(QPushButton, "btnContact"),  "action": Actions.BTN_PRESS },
            Items.ABOUT      : { "instance": self.theWindow.findChild(QPushButton, "btnAbout"),    "action": Actions.BTN_PRESS },
            Items.DARK_MODE  : { "instance": self.theWindow.findChild(QCheckBox, "boxDarkMode"),   "action": Actions.BOX_CHECK },
        }
