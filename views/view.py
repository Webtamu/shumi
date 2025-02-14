from abc import abstractmethod
from PyQt6.QtWidgets import QWidget
from helpers.signals import Signal

class View(QWidget):  

    @abstractmethod
    def __init__(self) -> None:
        super().__init__() 

    @abstractmethod
    def updateItemUI(self, aSignal: Signal) -> None:
        pass

    def toggleDarkMode(self, aSignal: Signal) -> None:
        if aSignal.theState: 
            with open("resources/dark_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
        else:
            self.theWindow.setStyleSheet("")
