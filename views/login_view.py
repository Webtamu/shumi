from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QCheckBox, QLabel

from views.view import View
from ui.labels import ClickableLabel
from helpers.helpers import Items, Actions, ViewState

class LoginView(View):
    # In LoginView class
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.LOGIN
        self.theWindow = uic.loadUi("qtdesigner/login_design.ui")
        self.initializeStyle()
    
        self.theItemMap = {
            Items.LOGIN_USERNAME : {"instance": self.theWindow.findChild(QLineEdit, "inputUsername"), "action": Actions.NONE},
            Items.LOGIN_PASSWORD : {"instance": self.theWindow.findChild(QLineEdit, "inputPassword"), "action": Actions.NONE},
            Items.LOGIN_STAY_SIGNED_IN : {"instance": self.theWindow.findChild(QCheckBox, "boxStaySignedIn"), "action": Actions.BOX_CHECK},
            Items.LOGIN_LOGIN : {"instance": self.theWindow.findChild(QPushButton, "btnLogin"), "action": Actions.BTN_PRESS},
            Items.LOGIN_CREATE_ACCOUNT : {"instance": ClickableLabel(self.theWindow.findChild(QLabel, "lblCreateAccount")), "action": Actions.LABEL_PRESS},
            Items.LOGIN_CANT_SIGN_IN : {"instance": ClickableLabel(self.theWindow.findChild(QLabel, "lblCantSignIn")), "action": Actions.LABEL_PRESS},
    }
            
         