from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items, ViewState
from helpers.logger import Logger


class PreferencesModel(Model):
    """
    This class houses user preferences data, which needs to be saved and
    reloaded on app reload.
    """

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.data_map = {
            Items.DARK_MODE: {"state": False,
                              "text": "Dark Mode"},

            Items.LANGUAGE: {"state": False,
                             "text": "Language"},

            Items.TIME: {"state": False,
                         "text": "Time"},
        }

        self.action_map = {}
        self.model_type = "Preferences"

    def __del__(self):
        """Log message when preferences data is being written to json."""
        Logger.info("Writing preferences data to json!")

    def update_model(self, signal: Signal) -> None:
        """
        Update the model based on the provided signal and notify controller.
        """
        if action := self.action_map.get(signal.item):
            action()

        item_entry = self.data_map[signal.item]
        item_entry["state"] = not item_entry["state"]

        signal.text = item_entry["text"]
        signal.state = item_entry["state"]
        signal.source = ViewState.ALL

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
