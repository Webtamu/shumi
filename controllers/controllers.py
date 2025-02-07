from PyQt6.QtCore import QObject, pyqtSlot
from abc import abstractmethod
from models.models import Model  
from views.view import View  

class Controller(QObject):

    @abstractmethod
    def __init__(self, aModel: Model, aView: View) -> None:
        super().__init__()

    # Slot from View (Initial Trigger), sending to Model for processing    
    @abstractmethod
    @pyqtSlot(str)
    def _handleViewResponse(self, aButtonName: str) -> None:
        pass

    # Slot from Model (Compute Response), sending to View for presentation
    @abstractmethod
    @pyqtSlot(str, bool, str)
    def _handleModelResponse(self, aButtonName: str, aState: bool, aText: str) -> None:
        pass
