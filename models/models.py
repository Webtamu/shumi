from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal
from abc import abstractmethod

from helpers.signals import Signal


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
        self.model_type = None

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
