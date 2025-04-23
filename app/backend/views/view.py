from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from abc import abstractmethod

from ..helpers import Signal, Items, Actions, ViewState


class View(QWidget):
    nav_signal = pyqtSignal(Signal)

    @abstractmethod
    def __init__(self) -> None:
        self.view_state = ViewState.DEFAULT
        self.window = None
        self.item_map = {}
        self.action_map = {
            Actions.BTN_PRESS: self.update_button,
            Actions.BOX_CHECK: self.update_box,
            Actions.LABEL_SET: self.update_label
        }
        super().__init__()

    def update_view(self, signal: Signal) -> None:
        if signal.item == Items.DARK_MODE:
            self.toggle_dark_mode(signal)

        item_entry = self.item_map.get(signal.item)
        if not item_entry:
            return

        if action := self.action_map.get(signal.action):
            action(item_entry["instance"], signal)

        if signal.nav:
            self.nav_signal.emit(signal)

    def toggle_dark_mode(self, signal: Signal) -> None:
        stylesheet_path = (
            "app/frontend/resources/dark_mode.qss" if signal.state else "app/frontend/resources/light_mode.qss"
        )
        with open(stylesheet_path, "r") as file:
            self.window.setStyleSheet(file.read())

    def initialize_style(self) -> None:
        with open("app/frontend/resources/light_mode.qss", "r") as file:
            self.window.setStyleSheet(file.read())

    def update_button(self, item: QWidget, signal: Signal) -> None:
        item.setChecked(signal.state)
        item.setText(signal.text)

    def update_box(self, item: QWidget, signal: Signal) -> None:
        item.setChecked(signal.state)
        item.setText(signal.text)

    def update_label(self, item: QWidget, signal: Signal) -> None:
        item.setText(signal.text)
