from PyQt6.QtCore import QObject
from abc import abstractmethod

from models.models import Model  
from views.view import View  
from helpers.signals import Signal
from helpers.helpers import Items

class Controller(QObject):

    @abstractmethod
    def __init__(self, model: Model, view: View) -> None:
        super().__init__()

    # Response from View (Initial Trigger), sending to Model for processing  
    @abstractmethod
    def handle_view_response(self, item_name: Items) -> None:
        pass

    # Response from Model (Compute Response), sending to View for presentation
    @abstractmethod
    def handle_model_response(self, signal: Signal) -> None:
        pass
