from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QPalette
from helpers.signals import Signal


class ClickableLabel(QLabel):
    clicked = pyqtSignal(Signal)

    def __init__(self, original_label: QLabel = None, signal: Signal = None):
        if not original_label:
            raise ValueError("Original label must be provided")
        parent = original_label.parent()
        super().__init__(parent)

        self.theSignal = signal
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to indicate clickable
        self.layout = parent.layout() if parent and parent.layout() else None
        # Copy properties from original label
        self._copy_label_properties(original_label)

        # Handle layout replacement with precision
        self._replace_in_layout(original_label)

        # Ensure label visibility
        self.setVisible(True)
        self.raise_()  # Bring to front

    def _copy_label_properties(self, original_label: QLabel):
        """Copy relevant properties from the original label."""
        self.original_rect = original_label.geometry()
        self.parent_pos = original_label.mapToParent(QPoint(0, 0))

        self.setText(original_label.text())
        self.setAlignment(original_label.alignment())
        self.setIndent(original_label.indent())
        self.setMargin(original_label.margin())
        self.setTextFormat(original_label.textFormat())
        self.setTextInteractionFlags(original_label.textInteractionFlags())
        self.setWordWrap(original_label.wordWrap())

        # Copy the exact font
        self.setFont(original_label.font())

        # Copy the exact color from the palette
        palette = original_label.palette()
        self.setPalette(palette)

        # Set background role
        self.setBackgroundRole(original_label.backgroundRole())
        self.setAutoFillBackground(original_label.autoFillBackground())

        # Apply default style (copy original style or create one)
        fg_color = palette.color(QPalette.ColorRole.WindowText).name()
        bg_color = palette.color(QPalette.ColorRole.Window).name()

        original_style = original_label.styleSheet()
        self.default_style = original_style if original_style else f"color: {fg_color}; background-color: {bg_color};"
        self.hover_style = f"{self.default_style} text-decoration: underline;"

        self.setStyleSheet(self.default_style)

    def _replace_in_layout(self, original_label: QLabel):
        """Replace the original label with the clickable label in the layout."""
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

        # Make the original label invisible but keep it for reference
        original_label.setVisible(False)
        self.original_label = original_label

    def enterEvent(self, event):
        """Handle mouse enter event for hover effect."""
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave event for removing hover effect."""
        self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Emit signal when clicked."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.theSignal:
                self.clicked.emit(self.theSignal)
        super().mousePressEvent(event)

    def set_signal(self, signal: Signal):
        """Set the signal to emit when clicked."""
        self.theSignal = signal
