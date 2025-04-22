from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton

from ..views import View
from ..helpers import Items, Actions, ViewState


class StatsView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.STATS
        self.window = uic.loadUi("app/frontend/qtdesigner/stats_design.ui")
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
        }
