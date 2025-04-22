from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QCheckBox

from ..views import View
from ..helpers import Items, Actions, ViewState


class SettingsView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.SETTINGS
        self.window = uic.loadUi("app/frontend/qtdesigner/settings_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.HOME: {
                "instance": self.window.findChild(QPushButton, "btnHome"),
                "action": Actions.BTN_PRESS
            },
            Items.SETTINGS: {
                "instance": self.window.findChild(QPushButton, "btnSettings"),
                "action": Actions.BTN_PRESS
            },
            Items.PROFILE: {
                "instance": self.window.findChild(QPushButton, "btnProfile"),
                "action": Actions.BTN_PRESS
            },
            Items.STATS: {
                "instance": self.window.findChild(QPushButton, "btnStats"),
                "action": Actions.BTN_PRESS
            },
            Items.REPORT_BUG: {
                "instance": self.window.findChild(QPushButton, "btnBug"),
                "action": Actions.BTN_PRESS
            },
            Items.CONTACT: {
                "instance": self.window.findChild(QPushButton, "btnContact"),
                "action": Actions.BTN_PRESS
            },
            Items.ABOUT: {
                "instance": self.window.findChild(QPushButton, "btnAbout"),
                "action": Actions.BTN_PRESS
            },
            Items.DARK_MODE: {
                "instance": self.window.findChild(QCheckBox, "boxDarkMode"),
                "action": Actions.BOX_CHECK
            },
            Items.SYNC: {
                "instance": self.window.findChild(QPushButton, "btnSync"),
                "action": Actions.BTN_PRESS
            },
        }
