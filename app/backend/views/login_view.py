from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QCheckBox, QLabel

from ..views import View
from ..ui import ClickableLabel
from ..helpers import Items, Actions, ViewState


class LoginView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.LOGIN
        self.window = uic.loadUi("app/frontend/qtdesigner/login_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.LOGIN_USERNAME: {
                "instance": self.window.findChild(QLineEdit, "inputUsername"),
                "action": Actions.NONE
            },
            Items.LOGIN_PASSWORD: {
                "instance": self.window.findChild(QLineEdit, "inputPassword"),
                "action": Actions.NONE
            },
            Items.LOGIN_STAY_SIGNED_IN: {
                "instance": self.window.findChild(QCheckBox, "boxStaySignedIn"),
                "action": Actions.BOX_CHECK
            },
            Items.LOGIN_LOGIN: {
                "instance": self.window.findChild(QPushButton, "btnLogin"),
                "action": Actions.BTN_PRESS
            },
            Items.LOGIN_CREATE_ACCOUNT: {
                "instance": ClickableLabel(self.window.findChild(QLabel, "lblCreateAccount")),
                "action": Actions.LABEL_PRESS
            },
            Items.LOGIN_CANT_SIGN_IN: {
                "instance": ClickableLabel(self.window.findChild(QLabel, "lblCantSignIn")),
                "action": Actions.LABEL_PRESS
            },
        }
