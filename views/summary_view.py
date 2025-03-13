from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton

from views.view import View
from helpers.helpers import Items, Actions, ViewState

class SummaryView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.SUMMARY
        self.theWindow = uic.loadUi("qtdesigner/summary_design.ui")

        self.theItemMap = {
            Items.BEGIN_TAKE  : { "instance": self.theWindow.findChild(QPushButton, "btnBeginTake"),    "action": Actions.BTN_PRESS },
        }
 
            
         