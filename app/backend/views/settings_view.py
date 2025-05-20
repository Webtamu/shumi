from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QCheckBox, QToolButton, QLabel, QComboBox

from ..views import View
from ..helpers import Items, Actions, ViewState


class SettingsView(View):
    def setup(self) -> None:
        self.view_state = ViewState.SETTINGS
        self.window = uic.loadUi("app/frontend/qtdesigner/settings_design.ui")
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
            Items.SETTINGS_PATH: {
                "instance": self.window.findChild(QToolButton, "toolButton"),
                "action": Actions.BTN_PRESS
            },
            Items.SETTINGS_PATH_SELECTED: {
                "instance": self.window.findChild(QLabel, "lblPathSelected"),
                "action": Actions.NONE
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
            Items.SETTINGS_INPUT_DEVICE: {
                "instance": self.window.findChild(QComboBox, "deviceInput"),
                "action": Actions.COMBO_SET
            },
            Items.SETTINGS_OUTPUT_DEVICE: {
                "instance": self.window.findChild(QComboBox, "deviceOutput"),
                "action": Actions.COMBO_SET
            }
        }
