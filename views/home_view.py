from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon

from ui.buttons import StartButton, SettingsButton, ProfileButton
from ui.heatmap import Heatmap 
from ui.streak import Placeholder
from views.view import View

class HomeView(View):
    def __init__(self) -> None:
        super().__init__()

        # General Window Info
        self.setWindowTitle("Jam App")
        self.setWindowIcon(QIcon("resources/orange_puffle.png")) 
        self.resize(800, 600)

        # Adding Components
        self.thePlaceholder = Placeholder("orange")
        self.theStartButton = StartButton()
        self.theSettingsButton = SettingsButton()
        self.theProfileButton = ProfileButton()
        self.theHeatmap = Heatmap()

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
        theCenterLayout.addWidget(self.theHeatmap.webView)
        theMainLayout.addLayout(theTopLayout)
        theMainLayout.addLayout(theCenterLayout)
        self.setLayout(theMainLayout)
        self.show()


    # Slot from Controller, updating button UI elements
    @pyqtSlot(str, bool, str)
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        # Update UI Elements
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)
            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (Checked: {aState})")
