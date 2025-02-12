from PyQt6.QtCore import pyqtSlot
from helpers.signals import Signal
from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Items, ViewState

class ApplicationController(Controller):
    def __init__(self, aModelList: list[Model], aViewList: list[View]) -> None:
        super().__init__(aModelList, aViewList)

        self.theAppModel = aModelList[0]
        self.thePreferencesModel = aModelList[1]
        self.theDataModel = aModelList[2]
        self.theViewMap = {}
        
        # Wiring up Model and View to the Controller
        self.theAppModel.theModelSignal.connect(self._handleModelResponse)

        # Connecting buttons to handlers
        for view in aViewList:
            for itemName, itemObject in view.theItemMap.items():
                itemObject.clicked.connect(lambda _, name=itemName, view=view.theViewState: self._handleViewResponse(name, view))
            self.theViewMap[view.theViewState] = view
         
    # Update from View (Initial Trigger), sending to Model for processing
    def _handleViewResponse(self, anItemName: Items, aViewSource: ViewState) -> None:
        self.theAppModel.updateItemState(anItemName, aViewSource)

    # Update from Model (Compute Response), sending to View for presentation
    @pyqtSlot(Signal)
    def _handleModelResponse(self, aSignal: Signal) -> None:
        theViewSource = self.theViewMap[aSignal.theSource]
        theViewSource.updateItemUI(aSignal)
