from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from ..helpers import Signal, Items, Actions, ViewState


class PyObj(QObject):
    web_signal = pyqtSignal(Signal)
    item_type = Items.DEFAULT
    view_state = ViewState.DEFAULT

    def __init__(self, item: Items, view_state: ViewState) -> None:
        super().__init__()
        self.item_type = item
        self.view_state = view_state

    @pyqtSlot(str)
    def sendData(self, data):
        self.web_signal.emit(Signal(
            item=self.item_type,
            action=Actions.WEB_BTN_PRESS,
            source=self.view_state,
            web={data}
        ))


class QWebWindow():
    def __init__(self, webengine: QWebEngineView, html: str, item: Items, view_state: ViewState) -> None:
        self.webengine = webengine
        self.channel = QWebChannel()
        self.obj = PyObj(item, view_state)
        self.channel.registerObject("pyObj", self.obj)
        self.webengine.page().setWebChannel(self.channel)
        self.webengine.setUrl(QUrl.fromLocalFile(html))
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.webengine.setSizePolicy(size_policy)
