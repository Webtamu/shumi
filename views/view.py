from abc import abstractmethod
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from helpers.signals import Signal
from helpers.helpers import Items, Colors

class View(QWidget):  

    @abstractmethod
    def __init__(self) -> None:
        super().__init__() 

    def updateView(self, aSignal: Signal) -> None:
        item = self.theItemMap.get(aSignal.theItem)

        if item:
            self.updateWidget(item, aSignal)

        self.theNavSignal.emit(aSignal)

        if aSignal.theItem == Items.DARK_MODE:
            self.toggleDarkMode(aSignal)

        # DEBUG STATEMENT
        if aSignal.theDebugTag:
            print(f"{Colors.YELLOW}Updated {aSignal.theItem}: {aSignal.theText} (State: {aSignal.theState}){Colors.RESET}")


    def updateWidget(self, item: QWidget, aSignal: Signal) -> None:
        if isinstance(item, QPushButton):
            item.setChecked(aSignal.theState)
            item.setText(aSignal.theText)
        elif isinstance(item, QLabel):
            item.setText(aSignal.theText)

    def toggleDarkMode(self, aSignal: Signal) -> None:
        if aSignal.theState: 
            with open("resources/dark_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
        else:
            self.theWindow.setStyleSheet("")
