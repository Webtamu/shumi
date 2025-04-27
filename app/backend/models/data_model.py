from ..services import DuckDBService, SupabaseService
from ..managers import ContextManager, SyncManager, SessionManager, AuthManager

from .models import Model
from ..helpers import Signal, Logger, Items, Actions

USER_DEFINED_TIME_PERIOD = 10


class DataModel(Model):
    """
    This class houses local storage that can be synced to cloud.
    """

    def __init__(self) -> None:
        super().__init__()
        self.data_map = {
            Items.SYNC: {"state": False, "text": "Sync"},
            Items.LOGIN_LOGIN: {"state": False, "text": "Login"},
            Items.START: {"state": False, "text": "Start Session"},
            Items.STOP: {"state": False, "text": "Stop Session"},
            Items.TIMER: {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
            Items.CREATE_ACCOUNT_CREATE: {"state": False, "text": "Create account"},
            Items.HOME_WELCOME: {"state": False, "text": ""},
            Items.HOME_CURRENT_STREAK: {"state": False, "text": ""},
            Items.HOME_DAILY_AVERAGE: {"state": False, "text": ""},
            Items.HOME_HIGHEST_STREAK: {"state": False, "text": ""},
            Items.PROFILE_EMAIL: {"state": False, "text": ""},
            Items.PROFILE_USERNAME: {"state": False, "text": ""},
            Items.PROFILE_USERNAME: {"state": False, "text": ""},
            Items.PROFILE_LOGOUT: {"state": False, "text": "Logout"},
        }

        self.model_type = "Data"

        self.local_database = DuckDBService()
        self.cloud_database = SupabaseService()

        self.context_manager = ContextManager()
        self.context_manager.set_callback(self.update_model)
        self.sync_manager = SyncManager(local_database=self.local_database,
                                        cloud_database=self.cloud_database,
                                        context=self.context_manager)
        self.session_manager = SessionManager(local_database=self.local_database,
                                              callback=self.update_model,
                                              context=self.context_manager)
        self.auth_manager = AuthManager(auth_service=self.cloud_database,
                                        callback=self.update_model,
                                        context=self.context_manager)

        self.action_map = {
            Items.SYNC: self.sync_manager.sync_to_cloud,
            Items.LOGIN_LOGIN: self.auth_manager.login,
            Items.PROFILE_LOGOUT: self.auth_manager.logout,
            Items.START: self.session_manager.begin_timer,
            Items.STOP: self.session_manager.stop_timer,
            Items.CREATE_ACCOUNT_CREATE: self.auth_manager.create_account,
        }

    def update_model(self, signal: Signal) -> None:
        """
        Update the model based on the given signal.
        """
        if action := self.action_map.get(signal.item):
            action(signal)

        item_entry = self.data_map[signal.item]
        if signal.action != Actions.LABEL_SET:  # Don't overwrite dynamic text
            item_entry["state"] = not item_entry["state"]
            signal.text = item_entry["text"]
            signal.state = item_entry["state"]

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
