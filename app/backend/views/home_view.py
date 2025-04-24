from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel

from ..views import View
from ..helpers import Items, Actions, ViewState


class HomeView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.HOME
        self.window = uic.loadUi("app/frontend/qtdesigner/home_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.START: {
                "instance": self.window.findChild(QPushButton, "btnStart"),
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
            Items.HOME_WELCOME: {
                "instance": self.window.findChild(QLabel, "lblWelcome"),
                "action": Actions.NONE
            },
            Items.HOME_CURRENT_STREAK: {
                "instance": self.window.findChild(QLabel, "lblCurrentStreak"),
                "action": Actions.NONE
            },
            Items.HOME_HIGHEST_STREAK: {
                "instance": self.window.findChild(QLabel, "lblHighestStreak"),
                "action": Actions.NONE
            },
            Items.HOME_DAILY_AVERAGE: {
                "instance": self.window.findChild(QLabel, "lblDailyAverage"),
                "action": Actions.NONE
            },
        }
