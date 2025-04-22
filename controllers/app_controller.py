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
    def __init__(self, model_list: list[Model], view_list: list[View]) -> None:
        super().__init__(model_list, view_list)

        self.model_list: list[Model] = model_list
        self.view_map: dict[ViewState, View] = {}

        # Wiring up Model signals to Controller
        for model in self.model_list:
            model.model_signal.connect(self.handle_model_response)

        # Connecting View items to Controller
        for view in view_list:
            self.connect_items(view)
            self.view_map[view.view_state] = view

    # Connect items based on action types
    def connect_items(self, view: View) -> None:
        for item_name, item_data in view.item_map.items():
            signal = Signal(
                item=item_name, 
                source=view.view_state, 
                action=item_data["action"]
            )
            Connections.connect_item(widget=item_data["instance"], signal=signal, function=self.handle_view_response)

    # Response from View (Initial Trigger), sending to Model for processing
    def handle_view_response(self, signal: Signal) -> None:
        if signal.item == Items.LOGIN_LOGIN:
            login_view = self.view_map.get(ViewState.LOGIN)
            signal.data = {
                "username": login_view.item_map[Items.LOGIN_USERNAME]["instance"].text(),
                "password": login_view.item_map[Items.LOGIN_PASSWORD]["instance"].text()
            }
        elif signal.item == Items.CREATE_ACCOUNT_CREATE:
            create_view = self.view_map.get(ViewState.CREATE)
            signal.data = {
                "user": create_view.item_map[Items.CREATE_ACCOUNT_USERNAME]["instance"].text(),
                "email": create_view.item_map[Items.CREATE_ACCOUNT_EMAIL]["instance"].text(),
                "pass": create_view.item_map[Items.CREATE_ACCOUNT_PASSWORD]["instance"].text(),
                "confirm_pass": create_view.item_map[Items.CREATE_ACCOUNT_PASSWORD_CONFIRM]["instance"].text()
            }

        for model in self.model_list:
            if model.can_handle(signal):
                model.update_model(signal)
                return
        Logger.error(f"Cannot handle request: {signal.item}")  

    # Response from Model (Compute Response), sending to View for presentation
    def handle_model_response(self, signal: Signal) -> None:
        if signal.source == ViewState.ALL:
            for view in self.view_map.values():
                view.update_view(signal)
        else:
            view_source = self.view_map[signal.source]
            view_source.update_view(signal)
