from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel

from ..views import View
from ..helpers import Items, Actions, ViewState


class SessionView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.SESSION
        self.window = uic.loadUi("app/frontend/qtdesigner/session_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.STOP: {
                "instance": self.window.findChild(QPushButton, "btnStop"),
                "action": Actions.BTN_PRESS
            },
            Items.TIMER: {
                "instance": self.window.findChild(QLabel, "lblTimer"),
                "action": Actions.NONE
            },
        }
