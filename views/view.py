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

    @abstractmethod
    def toggleDarkMode(self, state: bool) -> None:
        if state: 
            with open("resources/dark_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
        else:
            self.theWindow.setStyleSheet("")
