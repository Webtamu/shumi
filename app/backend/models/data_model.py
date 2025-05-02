from ..services import DuckDBService, SupabaseService
from ..managers import SyncManager, SessionManager, AuthManager

from .models import Model
from ..helpers import Signal, Logger, Items, Actions
from ..core.settings import USER_DEFINED_TIME_PERIOD


class DataModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.data_map = {
            # Authentication related items
            Items.LOGIN_LOGIN: {"state": False, "text": "Login", "nav": True},
            Items.PROFILE_LOGOUT: {"state": False, "text": "Logout", "nav": True},
            Items.CREATE_ACCOUNT_CREATE: {"state": False, "text": "Create account"},

            # Session related items
            Items.START: {"state": False, "text": "Start Session", "nav": True},
            Items.STOP: {"state": False, "text": "Stop Session", "nav": True},
            Items.BEGIN_TAKE: {"state": False, "text": "Begin Take", "nav": True},
            Items.TIMER: {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},

            # Sync related items
            Items.SYNC: {"state": False, "text": "Sync"},

            # Profile and stats display items
            Items.HOME_WELCOME: {"state": False, "text": ""},
            Items.HOME_CURRENT_STREAK: {"state": False, "text": ""},
            Items.HOME_DAILY_AVERAGE: {"state": False, "text": ""},
            Items.HOME_HIGHEST_STREAK: {"state": False, "text": ""},
            Items.PROFILE_EMAIL: {"state": False, "text": ""},
            Items.PROFILE_USERNAME: {"state": False, "text": ""},
        }

        self.model_type = "Data"

        self.local_database = DuckDBService()
        self.cloud_database = SupabaseService()

        self.sync_manager = SyncManager(local_database=self.local_database,
                                        cloud_database=self.cloud_database)
        self.session_manager = SessionManager(local_database=self.local_database)
        self.auth_manager = AuthManager(auth_service=self.cloud_database)

        self.action_map = {
            Items.SYNC: [self.sync_manager.sync_to_cloud],
            Items.LOGIN_LOGIN: [self.auth_manager.login,
                                self.sync_manager.update_streak_stats,
                                self.sync_manager.refresh_fields],
            Items.PROFILE_LOGOUT: [self.auth_manager.logout],
            Items.START: [self.session_manager.begin_timer],
            Items.STOP: [self.session_manager.stop_timer,
                         self.sync_manager.update_streak_stats,
                         self.sync_manager.refresh_fields],
            Items.BEGIN_TAKE: [self.session_manager.save_session_notes],
            Items.CREATE_ACCOUNT_CREATE: [self.auth_manager.create_account],
        }

    def update_model(self, signal: Signal) -> None:
        item_entry = self.data_map[signal.item]
        signal.nav = item_entry.get("nav", False)

        if actions := self.action_map.get(signal.item):
            for action in actions:
                action(signal)

        if signal.action != Actions.LABEL_SET:  # Don't overwrite dynamic text
            item_entry["state"] = not item_entry["state"]
            signal.text = item_entry["text"]
            signal.state = item_entry["state"]

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
