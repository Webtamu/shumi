from abc import abstractmethod
from PyQt6.QtWidgets import QWidget
from helpers.signals import Signal

class View(QWidget):  

    @abstractmethod
    def __init__(self) -> None:
        super().__init__() 

    @abstractmethod
    def doUpdateButtonUI(self, aSignal: Signal) -> None:
        pass