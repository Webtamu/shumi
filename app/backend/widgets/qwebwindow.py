from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebChannel import QWebChannel
from ..helpers import Signal, Items, Actions, ViewState
import json


class PyObj(QObject):
    web_signal = pyqtSignal(Signal)
    item_type = Items.DEFAULT
    view_state = ViewState.DEFAULT

    def __init__(self, item: Items, view_state: ViewState) -> None:
        super().__init__()
        self.item_type = item
        self.view_state = view_state
        self._web_page = None

    def set_web_page(self, page):
        self._web_page = page

    @pyqtSlot(str)
    def sendData(self, data):
        self.web_signal.emit(Signal(
            item=self.item_type,
            action=Actions.WEB_BTN_PRESS,
            source=self.view_state,
            web={"data": data}
        ))

    @pyqtSlot(str)
    def initializeComponent(self, data):
        self.web_signal.emit(Signal(
            item=self.item_type,
            action=Actions.WEB_COMPONENT_SET,
            source=self.view_state,
            web={"data": data}
        ))

    def send_to_js(self, data):
        if self._web_page:
            js_code = f"window.receiveDataFromPython({json.dumps(data)})"
            self._web_page.runJavaScript(js_code)


class QWebWindow():
    def __init__(self, webengine: QWebEngineView, html: str, item: Items, view_state: ViewState) -> None:
        self.webengine = webengine
        webengine.settings().setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        webengine.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.channel = QWebChannel()
        self.obj = PyObj(item, view_state)
        self.obj.set_web_page(self.webengine.page())
        self.channel.registerObject("pyObj", self.obj)
        self.webengine.page().setWebChannel(self.channel)
        self.webengine.setUrl(QUrl.fromLocalFile(html))

    def update_chart_data(self, data):
        self.obj.send_to_js(data)
