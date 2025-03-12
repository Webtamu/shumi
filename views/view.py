from abc import abstractmethod
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from helpers.signals import Signal
from helpers.helpers import Items

class View(QWidget):  

    @abstractmethod
    def __init__(self) -> None:
        super().__init__() 

    def updateItemUI(self, aSignal: Signal) -> None:
        if aSignal.theItem in self.theItemMap:
            theItem = self.theItemMap[aSignal.theItem]

            if isinstance(theItem, QPushButton):
                theItem.setChecked(aSignal.theState)
                theItem.setText(aSignal.theText)
            elif isinstance(theItem, QLabel):
                self.theItemMap[aSignal.theItem].setText(aSignal.theText)
               
        self.theNavSignal.emit(aSignal) 
        if aSignal.theItem == Items.DARK_MODE:
            self.toggleDarkMode(aSignal)

        # DEBUG STATEMENT
        if aSignal.theDebugTag:
            print(f"Updated {aSignal.theItem}: {aSignal.theText} (State: {aSignal.theState})") 

    def toggleDarkMode(self, aSignal: Signal) -> None:
        if aSignal.theState: 
            with open("resources/dark_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
        else:
            self.theWindow.setStyleSheet("")
