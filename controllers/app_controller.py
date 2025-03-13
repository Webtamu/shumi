from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget
from typing import Callable

from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Actions, ViewState
from helpers.signals import Signal

class ApplicationController(Controller):
    def __init__(self, aModelList: list[Model], aViewList: list[View]) -> None:
        super().__init__(aModelList, aViewList)

        self.theModelList: list[Model] = aModelList
        self.theViewMap: dict[ViewState, View] = {}

        self.theConnectionMap: dict[Actions, Callable] = {
            Actions.BTN_PRESS  : self.connectButton,
            Actions.BOX_CHECK  : self.connectBox,
        }

        # Wiring up Model signals to Controller
        for model in self.theModelList:
            model.theModelSignal.connect(self.handleModelResponse)

        # Connecting View items to Controller
        for view in aViewList:
            self.connectItems(view)
            self.theViewMap[view.theViewState] = view
    
    # Connect items based on action types
    def connectItems(self, aView: View) -> None:
          for item_name, item_data in aView.theItemMap.items():
                theSignal = Signal(theItem=item_name, theSource=aView.theViewState, theActionType=item_data["action"])

                if theConnection := self.theConnectionMap.get(theSignal.theActionType):
                    theConnection(aSignal=theSignal, anItem=item_data["instance"])

    def connectButton(self, aSignal: Signal, anItem: QWidget) -> None:
        anItem.clicked.connect(lambda _, signal=aSignal: self.handleViewResponse(signal))

    def connectBox(self, aSignal: Signal, anItem: QWidget) -> None:
        anItem.stateChanged.connect(lambda _, signal=aSignal: self.handleViewResponse(signal))
        
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
        

    