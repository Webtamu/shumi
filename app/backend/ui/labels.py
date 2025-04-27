from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QPalette
from ..helpers import Signal


class ClickableLabel(QLabel):
    clicked = pyqtSignal(Signal)

    def __init__(self, original_label: QLabel = None, signal: Signal = None):
        if not original_label:
            raise ValueError("Original label must be provided")
        parent = original_label.parent()
        super().__init__(parent)

        self.theSignal = signal
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout = parent.layout() if parent and parent.layout() else None
        self.copy_label_properties(original_label)
        self.replace_in_layout(original_label)
        self.setVisible(True)

    def copy_label_properties(self, original_label: QLabel):
        self.original_rect = original_label.geometry()
        self.parent_pos = original_label.mapToParent(QPoint(0, 0))
        self.setText(original_label.text())
        self.setAlignment(original_label.alignment())
        self.setIndent(original_label.indent())
        self.setMargin(original_label.margin())
        self.setTextFormat(original_label.textFormat())
        self.setTextInteractionFlags(original_label.textInteractionFlags())
        self.setWordWrap(original_label.wordWrap())
        self.setFont(original_label.font())
        palette = original_label.palette()
        self.setPalette(palette)
        self.setBackgroundRole(original_label.backgroundRole())
        self.setAutoFillBackground(original_label.autoFillBackground())
        fg_color = palette.color(QPalette.ColorRole.WindowText).name()
        bg_color = palette.color(QPalette.ColorRole.Window).name()
        original_style = original_label.styleSheet()
        self.default_style = original_style if original_style else f"color: {fg_color}; background-color: {bg_color};"
        self.hover_style = f"{self.default_style} text-decoration: underline;"
        self.setStyleSheet(self.default_style)

    def replace_in_layout(self, original_label: QLabel):
        if self.layout:
            index = -1
            for i in range(self.layout.count()):
                if self.layout.itemAt(i).widget() == original_label:
                    index = i
                    break

            if index != -1:
                self.layout.removeWidget(original_label)
                self.layout.insertWidget(index, self)

        self.setSizePolicy(original_label.sizePolicy())
        self.setGeometry(self.original_rect)
        self.move(self.parent_pos)

        original_label.setVisible(False)
        self.original_label = original_label

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.theSignal:
                self.clicked.emit(self.theSignal)
        super().mousePressEvent(event)

    def set_signal(self, signal: Signal):
        self.theSignal = signal
