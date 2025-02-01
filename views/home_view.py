from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon

from ui.buttons import *
from ui.streak import *

class cHomeView(QWidget):
    def __init__(self):
        super().__init__()

        # General Window Info
        self.setWindowTitle("Jam App")
        self.setWindowIcon(QIcon("resources/orange_puffle.png")) 
        self.resize(800, 600)

        # Adding Components
        self.thePlaceholder = cPlaceholder("orange")
        self.theStartButton = cStartButton()
        self.theSettingsButton = cSettingsButton()
        self.theProfileButton = cProfileButton()

        self.theButtonMap = {
            "btnStart": self.theStartButton,
            "btnSettings": self.theSettingsButton,
            "btnProfile": self.theProfileButton
        }

        # Layout related
        theMainLayout = QVBoxLayout()
        theTopLayout = QHBoxLayout()
        theCenterLayout = QVBoxLayout()
        theTopLayout.addStretch()
        theTopLayout.addWidget(self.theProfileButton)
        theTopLayout.addWidget(self.theSettingsButton) 
        theCenterLayout.addWidget(self.thePlaceholder)
        theCenterLayout.addWidget(self.theStartButton)
        theMainLayout.addLayout(theTopLayout)
        theMainLayout.addLayout(theCenterLayout)
        self.setLayout(theMainLayout)


    # Slot from Controller, updating UI elements
    @pyqtSlot(str, bool, str)
    def doUpdateButtonUI(self, aButtonName, aState, aText):
        # Update UI Elements
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)
            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (Checked: {aState})")
