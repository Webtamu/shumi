from PyQt6.QtWidgets import QWidget
from typing import Callable

from models.models import Model  
from views.view import View  
from controllers.controllers import Controller
from helpers.helpers import Actions, ViewState, Items
from helpers.signals import Signal
from helpers.connections import Connections
from helpers.logger import Logger

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
          for item_name, item_data in aView.theItemMap.items():
                theSignal = Signal(theItem=item_name, theSource=aView.theViewState, theActionType=item_data["action"])
                Connections.connectItem(anItem=item_data["instance"], aSignal=theSignal, aFunction=self.handleViewResponse)
        
    # Reponse from View (Initial Trigger), sending to Model for processing
    def handleViewResponse(self, aSignal: Signal) -> None:

        # Messy... need to find way to refactor this
        if aSignal.theItem == Items.LOGIN_LOGIN:
            theLoginView = self.theViewMap.get(ViewState.LOGIN)
            aSignal.theData = {"username": theLoginView.theItemMap[Items.LOGIN_USERNAME]["instance"].text(), 
                               "password": theLoginView.theItemMap[Items.LOGIN_PASSWORD]["instance"].text()}
        elif aSignal.theItem == Items.CREATE_ACCOUNT_CREATE:
            theCreateView = self.theViewMap.get(ViewState.CREATE)
            aSignal.theData = {"user": theCreateView.theItemMap[Items.CREATE_ACCOUNT_USERNAME]["instance"].text(), 
                               "email": theCreateView.theItemMap[Items.CREATE_ACCOUNT_EMAIL]["instance"].text(), 
                               "pass": theCreateView.theItemMap[Items.CREATE_ACCOUNT_PASSWORD]["instance"].text(), 
                               "confirm_pass": theCreateView.theItemMap[Items.CREATE_ACCOUNT_PASSWORD_CONFIRM]["instance"].text()}
        
        for model in self.theModelList:
            if model.canHandle(aSignal):
                model.updateModel(aSignal)
                return
        Logger.error("CANT HANDLE REQUEST") # TODO: make this a status or something later

    # Response from Model (Compute Response), sending to View for presentation
    def handleModelResponse(self, aSignal: Signal) -> None:
        if aSignal.theItem == Items.STOP:
            ...
            
        if aSignal.theSource == ViewState.ALL:
            for view in self.theViewMap.values():
                view.updateView(aSignal)
        else:
            theViewSource = self.theViewMap[aSignal.theSource]
            theViewSource.updateView(aSignal)
        

    