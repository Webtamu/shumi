from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QSettings
from ..helpers import Signal, Actions, Items, ViewState
import os

from ..core.eventbus import event_bus

QSETTINGS_ORG = "WEBTAMU"
QSETTINGS_APP = "SHUMI"
QSETTINGS_STORAGE_KEY = "storage_directory"


class StorageManager:
    def __init__(self):
        self.settings = QSettings(QSETTINGS_ORG, QSETTINGS_APP)
        self.current_path = self.settings.value(QSETTINGS_STORAGE_KEY, defaultValue="")
        if self.current_path:
            self.update_path()

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

    def get_directory(self):
        return self.current_path

    def set_directory(self, path: str):
        if os.path.isdir(path):
            self.current_path = path
            self.settings.setValue(QSETTINGS_STORAGE_KEY, path)
