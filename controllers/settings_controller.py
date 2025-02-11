from PyQt6.QtCore import pyqtSlot
from helpers.signals import Signal
from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Items

class SettingsController(Controller):
    def __init__(self, aModel: Model, aView: View) -> None:
        super().__init__(aModel, aView)
        self.theModel = aModel
        self.theView = aView

        # Wiring up Model and View to the Controller
        self.theModel.theModelSignal.connect(self._handleModelResponse)

        # Connecting buttons to handlers
        for itemName, itemObject in self.theView.theItemMap.items():
            itemObject.clicked.connect(lambda _, name=itemName: self._handleViewResponse(name))
         
    # Update from View (Initial Trigger), sending to Model for processing
    def _handleViewResponse(self, anItemName: Items) -> None:
        self.theModel.updateItemState(anItemName)

    # Update from Model (Compute Response), sending to View for presentation
    @pyqtSlot(Signal)
    def _handleModelResponse(self, aSignal: Signal) -> None:
        self.theView.updateItemUI(aSignal)

