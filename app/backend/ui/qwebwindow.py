from PyQt6.QtCore import QUrl, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
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
        try:
            parsed = json.loads(data)
            self.web_signal.emit(Signal(
                item=self.item_type,
                action=Actions.WEB_BTN_PRESS,
                source=self.view_state,
                web=parsed
            ))
        except json.JSONDecodeError:
            self.web_signal.emit(Signal(
                item=self.item_type,
                action=Actions.WEB_BTN_PRESS,
                source=self.view_state,
                web={"data": data}
            ))

    @pyqtSlot(str)
    def initializeComponent(self, data):
        try:
            parsed = json.loads(data)
            self.web_signal.emit(Signal(
                item=self.item_type,
                action=Actions.WEB_HEATMAP_SET,
                source=self.view_state,
                web=parsed
            ))
        except json.JSONDecodeError:
            self.web_signal.emit(Signal(
                item=self.item_type,
                action=Actions.WEB_HEATMAP_SET,
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
        self.channel = QWebChannel()
        self.obj = PyObj(item, view_state)
        self.obj.set_web_page(self.webengine.page())
        self.channel.registerObject("pyObj", self.obj)
        self.webengine.page().setWebChannel(self.channel)
        self.webengine.setUrl(QUrl.fromLocalFile(html))

        self.webengine.page().loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        if ok:
            pass
        # Commenting out for now, need to uniquely populate each item (heatmap vs bar)
            # self.update_chart_data({
            #     "data": [{"hour": 0, "value": 50, "session_id": 1},
            #              {"hour": 1, "value": 20, "session_id": 2},
            #              {"hour": 2, "value": 30, "session_id": 3},
            #              {"hour": 3, "value": 20, "session_id": 4},
            #              {"hour": 4, "value": 40, "session_id": 5},
            #              {"hour": 5, "value": 10, "session_id": 6},]
            # })

    def update_chart_data(self, data):
        self.obj.send_to_js(data)
