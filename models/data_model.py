from services.duckdb_service import DuckDBService
from services.supabase_service import SupabaseService
from managers.context_manager import ContextManager
from managers.sync_manager import SyncManager
from managers.session_manager import SessionManager
from managers.auth_manager import AuthManager
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items
from helpers.logger import Logger
from utils.timer import Timer

USER_DEFINED_TIME_PERIOD = 10


class DataModel(Model):
    """
    This class houses local storage that can be synced to cloud.
    """

    def __init__(self) -> None:
        super().__init__()
        self.local_database = DuckDBService()
        self.cloud_database = SupabaseService()

        self.context_manager = ContextManager()
        self.sync_manager = SyncManager(local_database=self.local_database,
                                        cloud_database=self.cloud_database,
                                        context=self.context_manager)
        self.session_manager = SessionManager(local_database=self.local_database,
                                              callback=self.update_model,
                                              context=self.context_manager)
        self.auth_manager = AuthManager(auth_service=self.cloud_database,
                                        context=self.context_manager)

        self.data_map = {
            Items.SYNC: {"state": False, "text": "Sync"},
            Items.LOGIN_LOGIN: {"state": False, "text": "Login"},
            Items.START: {"state": False, "text": "Start Session"},
            Items.STOP: {"state": False, "text": "Stop Session"},
            Items.TIMER: {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
            Items.CREATE_ACCOUNT_CREATE: {"state": False, "text": "Create account"},
        }

        self.action_map = {
            Items.SYNC: self.sync_manager.sync_to_cloud,
            Items.LOGIN_LOGIN: self.auth_manager.login,
            Items.START: self.session_manager.begin_timer,
            Items.STOP: self.session_manager.stop_timer,
            Items.CREATE_ACCOUNT_CREATE: self.auth_manager.create_account,
        }

        self.model_type = "Data"

    def update_model(self, signal: Signal) -> None:
        """
        Update the model based on the given signal.
        """
        if action := self.action_map.get(signal.item):
            action(signal)

        item_entry = self.data_map[signal.item]
        if signal.item != Items.TIMER:  # Don't overwrite dynamic text
            item_entry["state"] = not item_entry["state"]
            signal.text = item_entry["text"]
            signal.state = item_entry["state"]

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
