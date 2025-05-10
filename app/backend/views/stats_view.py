from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from ..views import View
from ..helpers import Items, Actions, ViewState, Signal, Logger

import os


class PyObj(QObject):    
    web_signal = pyqtSignal(Signal)

    @pyqtSlot(str)
    def sendData(self, data):
        Logger.critical(data)
        self.web_signal.emit(Signal(
            item=Items.STATS_GRAPH,
            action=Actions.WEB_BTN_PRESS,
            source=ViewState.STATS,
            web={data}
        ))


class QWebWindow():
    def __init__(self, webengine: QWebEngineView, html: str, view: View) -> None:
        self.webengine = webengine
        self.channel = QWebChannel(view)
        self.obj = PyObj(view)
        self.channel.registerObject("pyObj", self.obj)
        self.webengine.page().setWebChannel(self.channel)
        self.webengine.setUrl(QUrl.fromLocalFile(html))
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.webengine.setSizePolicy(size_policy)


class StatsView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.STATS
        self.window = uic.loadUi("app/frontend/qtdesigner/stats_design.ui")
        self.initialize_style()

        html_path = os.path.abspath("app/frontend/static/index.html")

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
                "instance": QWebWindow(self.window.findChild(QWebEngineView, "graphTest"), html_path, self),
                "action": Actions.WEB_BTN_PRESS
            }
        }
