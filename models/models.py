from PyQt6.QtCore import QObject
from abc import abstractmethod
from helpers.helpers import Items

class Model(QObject):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def updateItemState(self, anItem: Items) -> None:
        pass
