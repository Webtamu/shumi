from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtGui import QPalette, QColor
from helpers.signals import Signal

class ClickableLabel(QLabel):
    clicked = pyqtSignal(Signal)
    
    def __init__(self, original_label=None, aSignal=None):
        if not original_label:
            raise ValueError("Original label must be provided")
        
        # Initialize with the exact same parent as the original label
        parent = original_label.parent()
        super().__init__(parent)
        
        self.theSignal = aSignal
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to indicate clickable
        
        # Get the original label's layout
        self.layout = None
        if parent and parent.layout():
            self.layout = parent.layout()
        
        # Capture the original label's properties with maximum precision
        self.original_rect = original_label.geometry()
        self.parent_pos = original_label.mapToParent(QPoint(0, 0))
        
        # Copy ALL text properties
        self.setText(original_label.text())
        self.setAlignment(original_label.alignment())
        self.setIndent(original_label.indent())
        self.setMargin(original_label.margin())
        self.setTextFormat(original_label.textFormat())
        self.setTextInteractionFlags(original_label.textInteractionFlags())
        self.setWordWrap(original_label.wordWrap())
        
        # CRITICAL: Copy the exact font
        self.setFont(original_label.font())
        
        # CRITICAL: Copy the exact color from palette
        palette = original_label.palette()
        self.setPalette(palette)
        
        # CRITICAL: Set the background role to exactly match the original
        self.setBackgroundRole(original_label.backgroundRole())
        self.setAutoFillBackground(original_label.autoFillBackground())
        
        # Capture foreground, background colors from palette
        fg_color = palette.color(QPalette.ColorRole.WindowText).name()
        bg_color = palette.color(QPalette.ColorRole.Window).name()
        
        # Capture and apply the original style sheet
        original_style = original_label.styleSheet()
        
        # if a stylesheet exists, use it as base; otherwise create one with the palette colors
        if original_style:
            self.default_style = original_style
        else:
        # include background color explicitly
            self.default_style = f"color: {fg_color}; background-color: {bg_color};"
        
        # Add underline effect for hover while preserving all other styles
        self.hover_style = f"{self.default_style} text-decoration: underline;"
        
        # Apply the default style
        self.setStyleSheet(self.default_style)
        
        # Handle layout replacement with precision
        if self.layout:
            # Find the original label's position in the layout
            index = -1
            for i in range(self.layout.count()):
                if self.layout.itemAt(i).widget() == original_label:
                    index = i
                    break
            
            if index != -1:
                # Remove the original label from the layout
                self.layout.removeWidget(original_label)
                # Add the new clickable label to the same position in the layout
                self.layout.insertWidget(index, self)
        
        # Set exact same size policy
        self.setSizePolicy(original_label.sizePolicy())
        
        # Set the exact geometry
        self.setGeometry(self.original_rect)
        
        # Critical: Apply the exact positioning
        self.move(self.parent_pos)
        
        # Make original label invisible but keep it for reference
        original_label.setVisible(False)
        self.original_label = original_label
        
        # Ensure our label is visible
        self.setVisible(True)
        self.raise_()  # Bring to front
    
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
        
    def setSignal(self, aSignal):
        self.theSignal = aSignal
    