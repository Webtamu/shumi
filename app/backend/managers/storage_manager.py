from PyQt6.QtWidgets import QFileDialog
from ..helpers import Signal, Actions, Items, ViewState
import os

from ..core.eventbus import event_bus
from ..core.settings import get_settings, QSETTINGS_STORAGE_KEY, QSETTINGS_DARK_MODE_KEY


class StorageManager:
    def __init__(self):
        self.settings = get_settings()
        self.current_path: str = self.settings.value(QSETTINGS_STORAGE_KEY, defaultValue="")
        self.dark_mode: bool = self.settings.value(QSETTINGS_DARK_MODE_KEY, defaultValue=False, type=bool)
        if self.current_path:
            self.update_path()
        if self.dark_mode:
            self.update_dark_mode()

    def select_directory(self, signal=None):
        dir_path = QFileDialog.getExistingDirectory(None, "Select Storage Directory", self.current_path or "")
        if dir_path:
            self.set_directory(dir_path)
            self.update_path()

    def update_path(self) -> None:
        path_signal = Signal(
                item=Items.SETTINGS_PATH_SELECTED,
                text=self.current_path,
                action=Actions.LABEL_SET,
                source=ViewState.SETTINGS
            )
        event_bus.publish(path_signal)

    def update_dark_mode(self) -> None:
        dark_mode_signal = Signal(
                item=Items.DARK_MODE,
                text="Dark Mode",
                action=Actions.BOX_CHECK,
                source=ViewState.ALL,
                state=self.dark_mode
                )
        event_bus.publish(dark_mode_signal)

    def set_directory(self, path: str):
        if os.path.isdir(path):
            self.current_path = path
            self.settings.setValue(QSETTINGS_STORAGE_KEY, path)

    def set_dark_mode(self, signal: Signal) -> None:
        self.dark_mode = signal.state
        self.settings.setValue(QSETTINGS_DARK_MODE_KEY, self.dark_mode)
