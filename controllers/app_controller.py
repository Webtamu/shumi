from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QPushButton, QCheckBox
from helpers.signals import Signal
from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Actions, ViewState

class ApplicationController(Controller):
    def __init__(self, aModelList: list[Model], aViewList: list[View]) -> None:
        super().__init__(aModelList, aViewList)

        self.theModelList: list[Model] = aModelList
        self.theViewMap: dict[ViewState, View] = {}
        
        # Wiring up Model signals to Controller
        for model in self.theModelList:
            model.theModelSignal.connect(self.handleModelResponse)

        # Connecting View items to Controller
        for view in aViewList:
            self.connectItems(view)
            self.theViewMap[view.theViewState] = view
    
    # Connect items based on action types
    def connectItems(self, aView: View) -> None:
          for itemName, itemObject in aView.theItemMap.items():
                theSignal = Signal(theItem=itemName, theSource=aView.theViewState)
                if isinstance(itemObject, QPushButton):
                    theSignal.theActionType = Actions.BTN_PRESS
                    itemObject.clicked.connect(lambda _, signal=theSignal: self.handleViewResponse(signal))
                elif isinstance(itemObject, QCheckBox):
                    theSignal.theActionType = Actions.BOX_CHECK
                    itemObject.stateChanged.connect(lambda _, signal=theSignal: self.handleViewResponse(signal))

    # Reponse from View (Initial Trigger), sending to Model for processing
    def handleViewResponse(self, aSignal: Signal) -> None:
        for model in self.theModelList:
            if model.canHandle(aSignal):
                model.updateItemState(aSignal)
                return
        print("CANT HANDLE REQUEST") # TODO: make this a status or something later


    # Response from Model (Compute Response), sending to View for presentation
    @pyqtSlot(Signal)
    def handleModelResponse(self, aSignal: Signal) -> None:
        if aSignal.theSource == ViewState.ALL:
            for view in self.theViewMap.values():
                view.updateView(aSignal)
        else:
            theViewSource = self.theViewMap[aSignal.theSource]
            theViewSource.updateView(aSignal)
        
