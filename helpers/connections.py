from PyQt6.QtWidgets import QWidget
from typing import Callable

from helpers.signals import Signal
from helpers.helpers import Actions


class Connections:

    @staticmethod
    def connectButton(aSignal: Signal, anItem: QWidget, aFunction: Callable) -> None:
        anItem.clicked.connect(lambda _: aFunction(aSignal))

    @staticmethod
    def connectBox(aSignal: Signal, anItem: QWidget, aFunction: Callable) -> None:
        anItem.stateChanged.connect(lambda _: aFunction(aSignal))

    @staticmethod
    def connectItem(anItem: QWidget, aSignal: Signal, aFunction: Callable) -> None:
        theConnectionMap: dict[Actions, Callable] = {
            Actions.BTN_PRESS: Connections.connectButton,
            Actions.BOX_CHECK: Connections.connectBox,
            Actions.NONE: lambda *args, **kwargs: None,  # No-op lambda
        }

        theActionType = aSignal.theActionType

        if theActionType not in theConnectionMap:
            raise ValueError(f"Action '{theActionType}' is not defined in connection map.")
        
        theConnectionMap[theActionType](aSignal=aSignal, anItem=anItem, aFunction=aFunction)
