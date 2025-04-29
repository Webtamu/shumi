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

        # TEMP APP DATA STORE
        self.data_map = {
            Items.DARK_MODE: {"state": False, "text": "Dark Mode"},
            Items.LANGUAGE: {"state": False, "text": "Language"},
            Items.TIME: {"state": False, "text": "Time"},
            Items.LOGIN_STAY_SIGNED_IN: {"state": False, "text": "Stay signed in"},
            Items.SETTINGS_PATH: {"state": False, "text": "..."},
            Items.SETTINGS_PATH_SELECTED: {"state": False, "text": ""},
        }

        self.storage_manager = StorageManager(callback=self.update_model)

        self.action_map = {
            Items.SETTINGS_PATH: self.storage_manager.select_directory
        }

        self.model_type = "Preferences"

    def update_model(self, signal: Signal) -> None:
        if action := self.action_map.get(signal.item):
            action(signal)

        item_entry = self.data_map[signal.item]
        if signal.action != Actions.LABEL_SET:
            item_entry["state"] = not item_entry["state"]
            signal.text = item_entry["text"]
            signal.state = item_entry["state"]
            signal.source = ViewState.ALL

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
