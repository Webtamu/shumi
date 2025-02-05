from PyQt6.QtWidgets import QPushButton
from PyQt6 import uic
from views.view import View


class SessionView(View):
    def __init__(self) -> None:...
        
    # Response from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:...


