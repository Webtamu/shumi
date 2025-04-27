from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QPoint
from ..helpers import Signal


class PasswordLineEdit(QLineEdit):
    def __init__(self, original_lineedit: QLineEdit = None, signal: Signal = None):
        if not original_lineedit:
            raise ValueError("Original line edit must be provided")
        parent = original_lineedit.parent()
        super().__init__(parent)

        self.theSignal = signal
        self.original_rect = original_lineedit.geometry()
        self.parent_pos = original_lineedit.mapToParent(QPoint(0, 0))

        self.setEchoMode(QLineEdit.EchoMode.Password)

        self.copy_lineedit_properties(original_lineedit)
        self.replace_in_layout(original_lineedit)

        self.setVisible(True)

    def copy_lineedit_properties(self, original_lineedit: QLineEdit):
        self.setObjectName(original_lineedit.objectName())
        self.setText(original_lineedit.text())
        self.setPlaceholderText(original_lineedit.placeholderText())
        self.setAlignment(original_lineedit.alignment())
        self.setMaxLength(original_lineedit.maxLength())
        self.setFrame(original_lineedit.hasFrame())
        self.setClearButtonEnabled(original_lineedit.isClearButtonEnabled())
        self.setFont(original_lineedit.font())
        palette = original_lineedit.palette()
        self.setPalette(palette)
        self.setBackgroundRole(original_lineedit.backgroundRole())
        self.setAutoFillBackground(original_lineedit.autoFillBackground())
        self.setStyleSheet(original_lineedit.styleSheet())
        self.setEnabled(original_lineedit.isEnabled())
        self.setReadOnly(original_lineedit.isReadOnly())
        self.setMaximumSize(original_lineedit.maximumSize())
        self.setMinimumSize(original_lineedit.minimumSize())
        self.setSizePolicy(original_lineedit.sizePolicy())
        self.setToolTip(original_lineedit.toolTip())
        self.setWhatsThis(original_lineedit.whatsThis())
        self.setInputMethodHints(original_lineedit.inputMethodHints())
        self.setContextMenuPolicy(original_lineedit.contextMenuPolicy())
        self.setCursorPosition(original_lineedit.cursorPosition())

    def replace_in_layout(self, original_lineedit: QLineEdit):
        parent = original_lineedit.parent()
        layout = parent.layout() if parent and parent.layout() else None
        if layout:
            index = -1
            for i in range(layout.count()):
                if layout.itemAt(i).widget() == original_lineedit:
                    index = i
                    break
            if index != -1:
                layout.removeWidget(original_lineedit)
                layout.insertWidget(index, self)
        self.setGeometry(self.original_rect)
        self.move(self.parent_pos)
        original_lineedit.setVisible(False)
        self.original_lineedit = original_lineedit
