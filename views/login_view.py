from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QCheckBox

from views.view import View
from helpers.helpers import Items, Actions, ViewState

class LoginView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.LOGIN
        self.theWindow = uic.loadUi("qtdesigner/login_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.USERNAME        : { "instance": self.theWindow.findChild(QLineEdit, "inputUsername"),    "action": Actions.NONE },
            Items.PASSWORD        : { "instance": self.theWindow.findChild(QLineEdit, "inputPassword"),    "action": Actions.NONE },
            Items.STAY_SIGNED_IN  : { "instance": self.theWindow.findChild(QCheckBox, "boxStaySignedIn"),  "action": Actions.BOX_CHECK },
            Items.LOGIN           : { "instance": self.theWindow.findChild(QPushButton, "btnLogin"),       "action": Actions.BTN_PRESS },
        }
 
            
         