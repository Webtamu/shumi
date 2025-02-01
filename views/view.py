from abc import abstractmethod
from PyQt6.QtWidgets import QWidget

class View(QWidget):  

    @abstractmethod
    def __init__(self) -> None:
        super().__init__() 

    @abstractmethod
    def doUpdateButtonUI(self, aButtonName: str, aState: bool, aText: str) -> None:
        pass