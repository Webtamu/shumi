from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView

from ..views import View
from ..helpers import Items, Actions, ViewState
from ..widgets import QWebWindow
import os


class StatsView(View):
    def setup(self) -> None:
        self.view_state = ViewState.STATS
        self.window = uic.loadUi("app/frontend/qtdesigner/stats_design.ui")
        html_path = os.path.abspath("app/frontend/static/components/chart/index.html")
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
            Items.STATS_GRAPH: {
                "instance": QWebWindow(self.window.findChild(QWebEngineView, "graphTest"),
                                       html=html_path,
                                       item=Items.STATS_GRAPH,
                                       view_state=self.view_state),
                "action": Actions.WEB_BTN_PRESS
            }
        }
