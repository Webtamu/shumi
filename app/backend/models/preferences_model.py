from .models import Model
from ..helpers import Logger, Items, ViewState, Signal, Actions
from ..managers import StorageManager


class PreferencesModel(Model):
    """
    This class houses user preferences data, which needs to be saved and
    reloaded on app reload.
    """

    def __init__(self) -> None:
        super().__init__()
        self.model_type = "Preferences"
        self.data_map = {
            Items.DARK_MODE: {"state": False, "text": "Dark Mode"},
            Items.LANGUAGE: {"state": False, "text": "Language"},
            Items.TIME: {"state": False, "text": "Time"},
            Items.LOGIN_STAY_SIGNED_IN: {"state": False, "text": "Stay signed in"},
            Items.SETTINGS_PATH: {"state": False, "text": "..."},
            Items.SETTINGS_PATH_SELECTED: {"state": False, "text": ""},
        }

        self.storage_manager = StorageManager()

        self.action_map = {
            Items.SETTINGS_PATH: self.storage_manager.select_directory,
            Items.DARK_MODE: self.storage_manager.set_dark_mode,
        }

    def update_model(self, signal: Signal) -> None:
        item_entry = self.data_map[signal.item]
        if signal.action != Actions.LABEL_SET and signal.source != ViewState.ALL:
            if action := self.action_map.get(signal.item):
                action(signal)

            item_entry["state"] = signal.state
            signal.text = item_entry["text"]
            signal.source = ViewState.ALL

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
