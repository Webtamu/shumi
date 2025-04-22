import json

from services.duckdb_service import DuckDBService
from services.supabase_service import SupabaseService
from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items
from helpers.logger import Logger
from utils.timer import Timer

USER_DEFINED_TIME_PERIOD = 10

class DataModel(Model):
    """
    This class houses table data, which is local storage that can be synced to the cloud.
    """

    def __init__(self) -> None:
        super().__init__()

        self.database = SupabaseService()
        self.local_database = DuckDBService()

        self.data_map = {
            Items.SYNC: {"state": False, "text": "Sync"},
            Items.LOGIN_LOGIN: {"state": False, "text": "Login"},
            Items.START: {"state": False, "text": "Start Session"},
            Items.STOP: {"state": False, "text": "Stop Session"},
            Items.TIMER: {"state": False, "text": str(USER_DEFINED_TIME_PERIOD)},
            Items.CREATE_ACCOUNT_CREATE: {"state": False, "text": "Create Account"},
        }

        self.action_map = {
            Items.SYNC: self.sync_to_cloud,
            Items.LOGIN_LOGIN: self.login,
            Items.START: self.begin_timer,
            Items.STOP: self.stop_timer,
            Items.CREATE_ACCOUNT_CREATE: self.create_account,
        }

        self.model_type = "Data"
        self.user_id: str = None
        self.thread = None

    def sync_to_cloud(self, signal: Signal) -> None:
        """
        Sync unsynced data from the local database to the cloud.
        """
        Logger.debug(self.local_database.fetch_data('session'))

        unsynced_rows = self.local_database.collect_unsynced()
        synced_rows = self.database.upload_unsynced_sessions(unsynced_rows)
        self.local_database.mark_as_synced(synced_rows)

        Logger.debug(self.local_database.fetch_data('session'))

    def create_account(self, signal: Signal) -> None:
        """
        Create a new account if the provided data is valid.
        """
        username = signal.data.get("user")
        email = signal.data.get("email")
        password = signal.data.get("pass")
        password_confirm = signal.data.get("confirm_pass")

        if not username or not email or not password:
            Logger.error("Account creation failed: Missing required fields")
            return

        if password != password_confirm:
            Logger.error("Account creation failed: Passwords do not match")
            return

        if "@" not in email or "." not in email:
            Logger.error("Account creation failed: Invalid email format")
            return

        self.database.create_account(email, password, username)

    def login(self, signal: Signal) -> None:
        """
        Handle the login process for the user.
        """
        username = signal.data.get("username")
        password = signal.data.get("password")

        # TODO: Auto-login
        self.database.login(email="testuser@gmail.com", password="testpass")
        #self.database.login(email=username, password=password)

        if self.database.is_connected():
            user_info = self.database.get_user_info()
            self.user_id = user_info.user.id
            signal.nav = True

    def update_model(self, signal: Signal) -> None:
        """
        Update the model based on the given signal.
        """
        if action := self.action_map.get(signal.item):
            action(signal)

        item_entry = self.data_map[signal.item]
        if signal.item != Items.TIMER:  # Don't overwrite dynamic text (like timer)
            item_entry["state"] = not item_entry["state"]
            signal.text = item_entry["text"]
            signal.state = item_entry["state"]

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)

    def add_session(self, user_id, start_time, stop_time) -> None:
        """
        Add a new session to the local database.
        """
        self.local_database.insert_data(user_id, start_time, stop_time)

    def begin_timer(self, signal: Signal) -> None:
        """
        Begin the timer and start tracking the session.
        """
        signal.nav = True
        self.thread = Timer(USER_DEFINED_TIME_PERIOD)
        self.thread.timer_signal.connect(self.update_model)
        self.thread.start()

    def stop_timer(self, signal: Signal) -> None:
        """
        Stop the timer and save the session data.
        """
        signal.nav = True
        if self.thread:
            self.thread.stop()
            self.add_session(self.user_id, self.thread.start_time, self.thread.stop_time)
            self.thread = None

    def sync_to_cloud_test(self) -> None:
        """
        Sync local DuckDB unsynced sessions to Supabase and mark them as synced.
        """
        unsynced_sessions = self.local_database.collect_unsynced()

        if not unsynced_sessions:
            Logger.info(f'No unsynced sessions to upload.')
            return

        synced_ids = self.database.upload_unsynced_sessions(unsynced_sessions)

        if synced_ids:
            self.local_database.mark_as_synced(synced_ids)
            Logger.info(f'Synced {len(synced_ids)} session(s) to Supabase.')
        else:
            Logger.error(f"Failed to sync any sessions.")
