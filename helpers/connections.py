from PyQt6.QtWidgets import QWidget
from typing import Callable
from helpers.signals import Signal
from helpers.helpers import Actions
from ui.labels import ClickableLabel  # Import the ClickableLabel class


class Connections:
    @staticmethod
    def connect_button(signal: Signal, widget: QWidget, function: Callable) -> None:
        widget.clicked.connect(lambda _: function(signal))

    @staticmethod
    def connect_box(signal: Signal, widget: QWidget, function: Callable) -> None:
        widget.stateChanged.connect(lambda _: function(signal))

    @staticmethod
    def connect_label(signal: Signal, label: ClickableLabel, function: Callable) -> None:
        # For ClickableLabel, set the signal and connect its custom clicked signal
        label.set_signal(signal)
        label.clicked.connect(function)  # ClickableLabel emits the Signal object directly

    @staticmethod
    def connect_item(widget: QWidget, signal: Signal, function: Callable) -> None:
        # Different connection methods based on item type and action type
        if isinstance(widget, ClickableLabel) and signal.action == Actions.LABEL_PRESS:
            Connections.connect_label(signal=signal, label=widget, function=function)
            return
        # Use the standard connection map for other widget types
        connection_map: dict[Actions, Callable] = {
            Actions.BTN_PRESS: Connections.connect_button,
            Actions.LABEL_PRESS: Connections.connect_button,  # Still keep for backward compatibility
            Actions.BOX_CHECK: Connections.connect_box,
            Actions.NONE: lambda *args, **kwargs: None,  # No-op lambda
        }
        action = signal.action
        if action not in connection_map:
            raise ValueError(f"Action '{action}' is not defined in connection map.")
        connection_map[action](signal=signal, widget=widget, function=function)
