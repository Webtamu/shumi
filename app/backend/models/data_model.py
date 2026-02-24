from ..services import DuckDBService, SupabaseService
from ..managers import SyncManager, SessionManager, AuthManager

from .models import Model
from ..helpers import Signal, Logger, Items, ItemConfig, Actions
from ..core.settings import USER_DEFINED_TIME_PERIOD


class DataModel(Model):
    def __init__(self) -> None:
        super().__init__()
        self.data_map: dict[Items, ItemConfig] = {

            Items.LOGIN_LOGIN: ItemConfig(
                text="Login",
                nav=True
            ),
            Items.PROFILE_LOGOUT: ItemConfig(
                text="Logout",
                nav=True
            ),
            Items.CREATE_ACCOUNT_CREATE: ItemConfig(
                text="Create account"
            ),
            Items.START: ItemConfig(
                text="Start Session",
                nav=True
            ),
            Items.STOP: ItemConfig(
                text="Stop Session",
                nav=True
            ),
            Items.BEGIN_TAKE: ItemConfig(
                text="Begin Take",
                nav=True
            ),
            Items.TIMER: ItemConfig(
                text=str(USER_DEFINED_TIME_PERIOD)
            ),
            Items.SYNC: ItemConfig(
                text="Sync"
            ),
            Items.HOME_WELCOME: ItemConfig(),
            Items.HOME_CURRENT_STREAK: ItemConfig(),
            Items.HOME_DAILY_AVERAGE: ItemConfig(),
            Items.HOME_HIGHEST_STREAK: ItemConfig(),
            Items.PROFILE_EMAIL: ItemConfig(),
            Items.PROFILE_USERNAME: ItemConfig(),
            Items.HOME_HEATMAP: ItemConfig(),
            Items.STATS_GRAPH: ItemConfig(),
        }

        self.local_database = DuckDBService()
        self.cloud_database = SupabaseService()

        self.sync_manager = SyncManager(local_database=self.local_database,
                                        cloud_database=self.cloud_database)
        self.session_manager = SessionManager(local_database=self.local_database)
        self.auth_manager = AuthManager(auth_service=self.cloud_database)

        self.action_map = {
            Items.SYNC: [self.sync_manager.sync_to_cloud,
                         self.sync_manager.sync_from_cloud,
                         self.sync_manager.refresh_fields,],
            Items.LOGIN_LOGIN: [self.auth_manager.login,
                                self.sync_manager.update_streak_stats,
                                self.sync_manager.refresh_fields,],
            Items.PROFILE_LOGOUT: [self.auth_manager.logout],
            Items.START: [self.session_manager.begin_session],
            Items.STOP: [self.session_manager.stop_session,
                         self.sync_manager.update_streak_stats,
                         self.sync_manager.refresh_fields],
            Items.BEGIN_TAKE: [self.session_manager.save_session_notes,
                               self.session_manager.update_web_components],
            Items.CREATE_ACCOUNT_CREATE: [self.auth_manager.create_account],
            Items.HOME_HEATMAP: [self.session_manager.update_heatmap],
            Items.STATS_GRAPH: [self.session_manager.update_chart_data],
        }

    def update_model(self, signal: Signal) -> None:
        item_entry = self.data_map[signal.item]
        signal.nav = item_entry.nav

        if actions := self.action_map.get(signal.item):
            for action in actions:
                action(signal)

        if signal.action != Actions.LABEL_SET:  # Don't overwrite dynamic text
            item_entry.state = not item_entry.state
            signal.text = item_entry.text
            signal.state = item_entry.state

        Logger.debug(signal)
        self.model_signal.emit(signal)
