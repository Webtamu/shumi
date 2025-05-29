from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView

from ..views import View
from ..helpers import Items, Actions, ViewState
from ..widgets import QWebWindow, NavBar
import os

# Pet test
from PyQt6.QtGui import QMovie


class HomeView(View):
    def setup(self) -> None:
        self.view_state = ViewState.HOME
        self.window = uic.loadUi("app/frontend/qtdesigner/home_design.ui")
        html_path = os.path.abspath("app/frontend/static/components/heatmap/heatmap.html")
        nav_widget: NavBar = self.window.findChild(NavBar, "navBar")

        # Needs refactoring, implement MVC for multiple pets maybe defined from settings?
        pet_window = self.window.findChild(QLabel, "pet")
        movie = QMovie("app/frontend/qtdesigner/pet.gif")
        pet_window.setMovie(movie)
        movie.start()

        self.item_map = {
            Items.HOME_HEATMAP: {
                "instance": QWebWindow(self.window.findChild(QWebEngineView, "heatmapTest"),
                                       html=html_path,
                                       item=Items.HOME_HEATMAP,
                                       view_state=self.view_state),
                "action": Actions.WEB_BTN_PRESS
            },
            Items.START: {
                "instance": self.window.findChild(QPushButton, "btnStart"),
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
