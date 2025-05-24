from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6 import uic


class NavBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("app/frontend/qtdesigner/navbar.ui", self)

        self.btnHome: QPushButton = self.findChild(QPushButton, "btnHome")
        self.btnProfile: QPushButton = self.findChild(QPushButton, "btnProfile")
        self.btnSettings: QPushButton = self.findChild(QPushButton, "btnSettings")
        self.btnStats: QPushButton = self.findChild(QPushButton, "btnStats")
