from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon

from ui.buttons import StartButton, SettingsButton, ProfileButton
from ui.streak import Placeholder
from views.view import View

class SessionView(View):
    def __init__(self) -> None:...
        
    # Response from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:...


