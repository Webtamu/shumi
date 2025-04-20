from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel

from views.view import View
from helpers.helpers import Items, Actions, ViewState
from ui.labels import ClickableLabel

class CreateView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.CREATE
        self.theWindow = uic.loadUi("qtdesigner/create_account_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.CREATE_ACCOUNT_USERNAME           : { "instance": self.theWindow.findChild(QLineEdit, "inputUsernameCreation"),    "action": Actions.NONE },
            Items.CREATE_ACCOUNT_PASSWORD           : { "instance": self.theWindow.findChild(QLineEdit, "inputPasswordCreation"),    "action": Actions.NONE },
            Items.CREATE_ACCOUNT_PASSWORD_CONFIRM   : { "instance": self.theWindow.findChild(QLineEdit, "inputPasswordCreationConfirm"),    "action": Actions.NONE },
            Items.CREATE_ACCOUNT_EMAIL              : { "instance": self.theWindow.findChild(QLineEdit, "inputEmailCreation"),       "action": Actions.NONE },
            Items.CREATE_ACCOUNT_CREATE               : { "instance": self.theWindow.findChild(QPushButton, "btnCreateAccount"),       "action": Actions.BTN_PRESS },
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT : {"instance": ClickableLabel(self.theWindow.findChild(QLabel, "lblAlreadyHaveAccount")), "action": Actions.LABEL_PRESS},
        }
 
            
         