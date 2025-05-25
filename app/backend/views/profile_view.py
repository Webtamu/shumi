from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel

from ..views import View
from ..helpers import Items, Actions, ViewState
from ..widgets import NavBar


class ProfileView(View):
    def setup(self) -> None:
        self.view_state = ViewState.PROFILE
        self.window = uic.loadUi("app/frontend/qtdesigner/profile_design.ui")
        nav_widget: NavBar = self.window.findChild(NavBar, "navBar")
        self.item_map = {
            Items.HOME: {
                "instance": nav_widget.btnHome,
                "action": Actions.BTN_PRESS
            },
            Items.SETTINGS: {
                "instance": nav_widget.btnSettings,
                "action": Actions.BTN_PRESS
            },
            Items.PROFILE: {
                "instance": nav_widget.btnProfile,
                "action": Actions.BTN_PRESS
            },
            Items.STATS: {
                "instance": nav_widget.btnStats,
                "action": Actions.BTN_PRESS
            },
            Items.PROFILE_LOGOUT: {
                "instance": self.window.findChild(QPushButton, "btnLogout"),
                "action": Actions.BTN_PRESS
            },
            Items.PROFILE_USERNAME: {
                "instance": self.window.findChild(QLabel, "lblUsername"),
                "action": Actions.NONE
            },
            Items.PROFILE_EMAIL: {
                "instance": self.window.findChild(QLabel, "lblEmail"),
                "action": Actions.NONE
            },
        }
