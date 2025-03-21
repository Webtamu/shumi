from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from helpers.signals import Signal  

class ClickableLabel(QLabel):
    clicked = pyqtSignal(Signal) 

    def __init__(self, parent=None, aSignal: Signal = None):
        super().__init__(parent)
        self.theSignal = aSignal  

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.theSignal:
                self.clicked.emit(self.theSignal) 