from PyQt6.QtWidgets import QWidget
from typing import Callable
from helpers.signals import Signal
from helpers.helpers import Actions
from ui.labels import ClickableLabel  # Import the ClickableLabel class

class Connections:
    @staticmethod
    def connectButton(aSignal: Signal, anItem: QWidget, aFunction: Callable) -> None:
        anItem.clicked.connect(lambda _: aFunction(aSignal))
    
    @staticmethod
    def connectBox(aSignal: Signal, anItem: QWidget, aFunction: Callable) -> None:
        anItem.stateChanged.connect(lambda _: aFunction(aSignal))
    
    @staticmethod
    def connectLabel(aSignal: Signal, anItem: ClickableLabel, aFunction: Callable) -> None:
        # For ClickableLabel, set the signal and connect its custom clicked signal
        anItem.setSignal(aSignal)
        anItem.clicked.connect(aFunction)  # ClickableLabel emits the Signal object directly
    
    @staticmethod
    def connectItem(anItem: QWidget, aSignal: Signal, aFunction: Callable) -> None:
        # Different connection methods based on item type and action type
        if isinstance(anItem, ClickableLabel) and aSignal.theActionType == Actions.LABEL_PRESS:
            Connections.connectLabel(aSignal=aSignal, anItem=anItem, aFunction=aFunction)
            return
        
        # Use the standard connection map for other widget types
        theConnectionMap: dict[Actions, Callable] = {
            Actions.BTN_PRESS: Connections.connectButton,
            Actions.LABEL_PRESS: Connections.connectButton,  # Still keep for backward compatibility
            Actions.BOX_CHECK: Connections.connectBox,
            Actions.NONE: lambda *args, **kwargs: None,  # No-op lambda
        }
        
        theActionType = aSignal.theActionType
        if theActionType not in theConnectionMap:
            raise ValueError(f"Action '{theActionType}' is not defined in connection map.")
        
        theConnectionMap[theActionType](aSignal=aSignal, anItem=anItem, aFunction=aFunction)