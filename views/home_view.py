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
        self.theHeatmap = Heatmap()
        self.theButtonMap = {
            "btnStart": StartButton(),
            "btnSettings": SettingsButton(),
            "btnProfile": ProfileButton(),
        }

        # Layout related
        theMainLayout = QVBoxLayout()
        theTopLayout = QHBoxLayout()
        theCenterLayout = QVBoxLayout()
        theTopLayout.addStretch()
        theTopLayout.addWidget(self.theButtonMap["btnProfile"])
        theTopLayout.addWidget(self.theButtonMap["btnSettings"]) 
        theCenterLayout.addWidget(self.thePlaceholder)
        theCenterLayout.addWidget(self.theButtonMap["btnStart"])
        theCenterLayout.addWidget(self.theHeatmap)
        theMainLayout.addLayout(theTopLayout)
        theMainLayout.addLayout(theCenterLayout)
        self.setLayout(theMainLayout)
        self.show()


    # Update from Controller, updating button UI elements
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        if aButtonName in self.theButtonMap:
            self.theButtonMap[aButtonName].setChecked(aState)
            self.theButtonMap[aButtonName].setText(aText)
            # DEBUG STATEMENT
            print(f"Updated {aButtonName}: {aText} (State: {aState})")
