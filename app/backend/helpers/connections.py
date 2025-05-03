from PyQt6.QtWidgets import QWidget, QComboBox
from typing import Callable
from ..helpers import Signal, Actions
from ..ui import ClickableLabel


class Connections:
    @staticmethod
    def connect_button(signal: Signal, widget: QWidget, function: Callable) -> None:
        widget.clicked.connect(lambda _: function(signal))

    @staticmethod
    def connect_box(signal: Signal, widget: QWidget, function: Callable) -> None:
        widget.stateChanged.connect(
            lambda state: function(Signal(
                item=signal.item,
                action=signal.action,
                text=signal.text,
                source=signal.source,
                state=bool(state),  # crucial
                nav=signal.nav,
                debug=signal.debug
            ))
        )

    @staticmethod
    def connect_combo(signal: Signal, widget: QComboBox, function: Callable) -> None:
        widget.currentIndexChanged.connect(
            lambda index: function(Signal(
                item=signal.item,
                action=signal.action,
                text=widget.itemText(index),
                source=signal.source,
                nav=signal.nav,
                debug=signal.debug
            ))
        )

    @staticmethod
    def connect_label(signal: Signal, widget: ClickableLabel, function: Callable) -> None:
        widget.set_signal(signal)
        widget.clicked.connect(function)

    @staticmethod
    def connect_item(widget: QWidget, signal: Signal, function: Callable) -> None:
        connection_map: dict[Actions, Callable] = {
            Actions.BTN_PRESS: Connections.connect_button,
            Actions.LABEL_PRESS: Connections.connect_label,
            Actions.BOX_CHECK: Connections.connect_box,
            Actions.COMBO_SET: Connections.connect_combo,
            Actions.NONE: lambda *args, **kwargs: None,
        }
        if action := connection_map.get(signal.action):
            action(signal=signal, widget=widget, function=function)
        else:
            raise ValueError(f"Action '{action}' is not defined in connection map.")
