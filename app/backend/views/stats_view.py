from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

from ..views import View
from ..helpers import Items, Actions, ViewState

import os


class StatsView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.STATS
        self.window = uic.loadUi("app/frontend/qtdesigner/stats_design.ui")
        self.initialize_style()

        html_path = os.path.abspath("app/frontend/experiments/index.html")
        self.webEngineView = self.window.findChild(QWebEngineView, "graphTest")
        self.webEngineView.setUrl(QUrl.fromLocalFile(html_path))

        # Make sure the QWebEngineView fills the layout
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.webEngineView.setSizePolicy(size_policy)

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
