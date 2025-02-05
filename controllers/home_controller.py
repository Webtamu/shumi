from PyQt6.QtCore import pyqtSlot
from models.models import Model  
from views.view import View  
from controllers.controllers import Controller

class HomeController(Controller):
    def __init__(self, aModel: Model, aView: View) -> None:
        super().__init__(aModel, aView)
        self.theModel = aModel
        self.theView = aView

        # Wiring up Model and View to the Controller
        self.theModel.theButtonSignal.connect(self._handleModelResponse)

        # Connecting buttons to handlers
        for btnName, btnObject in self.theView.theButtonMap.items():
            btnObject.clicked.connect(lambda _, name=btnName: self._handleViewResponse(name))
         
    # Update from View (Initial Trigger), sending to Model for processing
    def _handleViewResponse(self, aButtonName: str) -> None:
        self.theModel.doUpdateButtonState(aButtonName)

    # Update from Model (Compute Response), sending to View for presentation
    @pyqtSlot(str, bool, str)
    def _handleModelResponse(self, aButtonName: str, aState: bool, aText: str) -> None:
        self.theView.doUpdateButtonUI(aButtonName, aState, aText)
