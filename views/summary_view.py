from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton

from views.view import View
from helpers.helpers import Items, Actions, ViewState


class SummaryView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.SUMMARY
        self.window = uic.loadUi("qtdesigner/summary_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.BEGIN_TAKE: {
                "instance": self.window.findChild(QPushButton, "btnBeginTake"),
                "action": Actions.BTN_PRESS
            },
        }
