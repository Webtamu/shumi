from PyQt6.QtCore import QObject, pyqtSlot
from abc import abstractmethod
from models.models import Model  
from views.view import View  
from helpers.signals import Signal
from helpers.helpers import Items

class Controller(QObject):

    @abstractmethod
    def __init__(self, aModel: Model, aView: View) -> None:
        super().__init__()

    # Reponse from View (Initial Trigger), sending to Model for processing  
    @abstractmethod
    @pyqtSlot(str)
    def _handleViewResponse(self, anItemName: Items) -> None:
        pass

    # Response from Model (Compute Response), sending to View for presentation
    @abstractmethod
    @pyqtSlot(Signal)
    def _handleModelResponse(self, aSignal: Signal) -> None:
        pass
