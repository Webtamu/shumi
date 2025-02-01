
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
)

from PyQt6.QtGui import QIcon

from ui.buttons import *
from ui.streak import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jam App")
        self.setWindowIcon(QIcon("resources/Orange_Puffle.png")) 
        self.resize(800, 600)

        # TODO: Refactor into view
        theMainLayout = QVBoxLayout()
        theTopLayout = QHBoxLayout()
        theCenterLayout = QVBoxLayout()

        self.thePlaceholder = cPlaceholder("orange")
        self.theStartButton = cStartButton()
        self.theSettingsButton = cSettingsButton()
        self.theProfileButton = cProfileButton()

        theTopLayout.addStretch()
        theTopLayout.addWidget(self.theProfileButton)
        theTopLayout.addWidget(self.theSettingsButton) 
        
        theCenterLayout.addWidget(self.thePlaceholder)
        theCenterLayout.addWidget(self.theStartButton)
      
        theMainLayout.addLayout(theTopLayout)
        theMainLayout.addLayout(theCenterLayout)

        self.setLayout(theMainLayout)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()