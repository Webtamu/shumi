from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget

class Placeholder(QWidget):
    def __init__(self, aColor: QColor) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        thePalette = self.palette()
        thePalette.setColor(QPalette.ColorRole.Window, QColor(aColor))
        self.setPalette(thePalette)