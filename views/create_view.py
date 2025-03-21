from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QCheckBox

from views.view import View
from helpers.helpers import Items, Actions, ViewState

class CreateView(View):
    def __init__(self) -> None:
        super().__init__()
        self.theViewState = ViewState.CREATE
        self.theWindow = uic.loadUi("qtdesigner/create_account_design.ui")
        self.initializeStyle()

        self.theItemMap = {
            Items.USERNAME_CREATION           : { "instance": self.theWindow.findChild(QLineEdit, "inputUsernameCreation"),    "action": Actions.NONE },
            Items.PASSWORD_CREATION           : { "instance": self.theWindow.findChild(QLineEdit, "inputPasswordCreation"),    "action": Actions.NONE },
            Items.PASSWORD_CREATION_CONFIRM   : { "instance": self.theWindow.findChild(QLineEdit, "inputPasswordCreation"),    "action": Actions.NONE },
            Items.EMAIL_CREATION              : { "instance": self.theWindow.findChild(QLineEdit, "inputEmailCreation"),       "action": Actions.NONE },
            Items.CREATE_ACCOUNT              : { "instance": self.theWindow.findChild(QPushButton, "btnCreateAccount"),       "action": Actions.BTN_PRESS },
        }
 
            
         