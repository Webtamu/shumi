from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QPlainTextEdit

from ..views import View
from ..helpers import Items, Actions, ViewState


class SummaryView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.SUMMARY
        self.window = uic.loadUi("app/frontend/qtdesigner/summary_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.BEGIN_TAKE: {
                "instance": self.window.findChild(QPushButton, "btnBeginTake"),
                "action": Actions.BTN_PRESS
            },
            Items.SUMMARY_NOTES: {
                "instance": self.window.findChild(QPlainTextEdit, "editNotes"),
                "action": Actions.NONE
            }
        }
