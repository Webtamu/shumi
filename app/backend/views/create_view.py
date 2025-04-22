from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel

from ..views import View
from ..helpers import Items, Actions, ViewState
from ..ui import ClickableLabel


class CreateView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_state = ViewState.CREATE
        self.window = uic.loadUi("app/frontend/qtdesigner/create_account_design.ui")
        self.initialize_style()

        self.item_map = {
            Items.CREATE_ACCOUNT_USERNAME: {
                "instance": self.window.findChild(QLineEdit, "inputUsernameCreation"),
                "action": Actions.NONE
            },
            Items.CREATE_ACCOUNT_PASSWORD: {
                "instance": self.window.findChild(QLineEdit, "inputPasswordCreation"),
                "action": Actions.NONE
            },
            Items.CREATE_ACCOUNT_PASSWORD_CONFIRM: {
                "instance": self.window.findChild(QLineEdit, "inputPasswordCreationConfirm"),
                "action": Actions.NONE
            },
            Items.CREATE_ACCOUNT_EMAIL: {
                "instance": self.window.findChild(QLineEdit, "inputEmailCreation"),
                "action": Actions.NONE
            },
            Items.CREATE_ACCOUNT_CREATE: {
                "instance": self.window.findChild(QPushButton, "btnCreateAccount"),
                "action": Actions.BTN_PRESS
            },
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT: {
                "instance": ClickableLabel(
                    self.window.findChild(QLabel, "lblAlreadyHaveAccount")
                ),
                "action": Actions.LABEL_PRESS
            },
        }
