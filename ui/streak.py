from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget


class Placeholder(QWidget):
    def __init__(self, color: QColor) -> None:
        super().__init__()
        self.setAutoFillBackground(True)

        # Get the widget's current palette
        palette = self.palette()

        # Set the background color
        palette.setColor(QPalette.ColorRole.Window, color)

        # Apply the new palette
        self.setPalette(palette)
