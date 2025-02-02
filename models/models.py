from PyQt6.QtCore import QObject
from abc import abstractmethod

class Model(QObject):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def doUpdateButtonState(self, aButtonName: str) -> None:
        pass
