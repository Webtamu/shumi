from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget

class cPlaceholder(QWidget):
    def __init__(self, aColor):
        super().__init__()
        self.setAutoFillBackground(True)

        thePalette = self.palette()
        thePalette.setColor(QPalette.ColorRole.Window, QColor(aColor))
        self.setPalette(thePalette)