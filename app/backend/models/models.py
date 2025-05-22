from PyQt6.QtCore import QObject, pyqtSignal
from abc import abstractmethod

from ..helpers import Signal


class Model(QObject):
    """
    Abstract base class for all models in the application.
    Models handle data and notify controllers of changes via signals.
    """

    model_signal = pyqtSignal(Signal)

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()
        self.data_map = {}
        self.action_map = {}

    def can_handle(self, signal: Signal) -> bool:
        """
        Check if the model can handle the given signal.
        """
        return signal.item in self.data_map

    @abstractmethod
    def update_model(self, signal: Signal) -> None:
        """
        Update the model with the given signal.
        """
        ...
