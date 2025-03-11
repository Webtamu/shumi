from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QPushButton, QCheckBox
from helpers.signals import Signal
from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Items, ViewState, Actions

class ApplicationController(Controller):
    def __init__(self, aModelList: list[Model], aViewList: list[View]) -> None:
        super().__init__(aModelList, aViewList)

        self.theModelList = aModelList
        self.theViewMap = {}
        
        # Wiring up Model and View to the Controller
        for model in self.theModelList:
            model.theModelSignal.connect(self._handleModelResponse)

        # Connecting buttons to handlers
        for view in aViewList:
            for itemName, itemObject in view.theItemMap.items():
                theSignal = Signal(theItem=itemName, theSource=view.theViewState)
                if isinstance(itemObject, QPushButton):
                    theSignal.theActionType = Actions.BTN_PRESS
                    itemObject.clicked.connect(lambda _, signal=theSignal: self._handleViewResponse(signal))
                elif isinstance(itemObject, QCheckBox):
                    theSignal.theActionType = Actions.BOX_CHECK
                    itemObject.stateChanged.connect(lambda _, signal=theSignal: self._handleViewResponse(signal))
            self.theViewMap[view.theViewState] = view
         
    # Update from View (Initial Trigger), sending to Model for processing
    def _handleViewResponse(self, aSignal: Signal) -> None:
        for model in self.theModelList:
            if model.canHandle(aSignal):
                model.updateItemState(aSignal)
                return
        print("CANT HANDLE REQUEST") # TODO: make this a status or something later


    # Update from Model (Compute Response), sending to View for presentation
    @pyqtSlot(Signal)
    def _handleModelResponse(self, aSignal: Signal) -> None:
        if aSignal.theBroadcastTag:
            for view in self.theViewMap.values():
                view.updateItemUI(aSignal)
        else:
            theViewSource = self.theViewMap[aSignal.theSource]
            theViewSource.updateItemUI(aSignal)
        
