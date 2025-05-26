from ..helpers import Logger, Signal, Items, Actions, ViewState
from ..services import DuckDBService, SupabaseService
from datetime import datetime
import re
from ..core.context import app_context
from ..core.eventbus import event_bus


class SyncManager:
    def __init__(self, local_database: DuckDBService, cloud_database: SupabaseService):
        self.local_database = local_database
        self.cloud_database = cloud_database

    def sync_to_cloud(self, signal: Signal = None) -> None:
        """
        Sync unsynced data from the local database to the cloud.
        """

        unsynced_rows = self.local_database.collect_unsynced()
        print(unsynced_rows)
        if not unsynced_rows:
            Logger.info('No unsynced sessions to upload.')
            return

        synced_rows = self.cloud_database.upload_unsynced_sessions(unsynced_rows)
        print(synced_rows)
        if synced_rows:
            self.local_database.mark_as_synced(synced_rows)
            Logger.info(f'Synced {len(synced_rows)} session(s) to Supabase.')
        else:
            Logger.error('Failed to sync any sessions.')

    def parse_iso_datetime(self, dt_str):
        # Handle nanoseconds/microseconds of variable length
        if '.' in dt_str:
            dt_str = re.sub(r'\.(\d+)', lambda m: '.%s' % m.group(1).ljust(6, '0')[:6], dt_str)
        return datetime.fromisoformat(dt_str)

    def sync_from_cloud(self, signal: Signal = None) -> None:
        """
        Sync cloud data to local DuckDB by replacing all of the user's sessions
        with what exists in the cloud database.
        """

        # Get current authenticated user
        user = self.cloud_database.get_user_info()
        Logger.debug(f"Fetching sessions for {user.user.user_metadata.get('full_name')}.")
        if not user or not user.user:
            Logger.error("No authenticated user for cloud sync")
            return

        cloud_sessions = self.cloud_database.fetch_data("study_sessions").data
        print(cloud_sessions)
        self.local_database.con.raw_sql(f"DELETE FROM session WHERE user_id = '{user.user.id}'")

        for session in cloud_sessions:
            try:
                self.local_database.insert_data(
                    user_id=session['user_id'],
                    start_time=self.parse_iso_datetime(session['timestamp_start']),
                    stop_time=self.parse_iso_datetime(session['timestamp_stop']),
                    synced=True
                )
            except Exception as e:
                Logger.error(f"Failed to insert session {session.get('session_id')}: {e}")

        Logger.info(f"Synced {len(cloud_sessions)} session(s) from Supabase")

    def refresh_fields(self, signal: Signal = None):
        signals = self.generate_field_signals()
        for signal in signals:
            event_bus.publish(signal)

    def update_streak_stats(self, signal: Signal = None):
        app_context.current_streak = self.local_database.get_current_streak(app_context.user_id, "UTC")
        app_context.highest_streak = self.local_database.get_highest_streak(app_context.user_id, "UTC")
        app_context.daily_average = self.local_database.get_average_session_minutes(app_context.user_id)

    def generate_field_signals(self) -> list[Signal]:
        return [
            Signal(
                item=Items.HOME_WELCOME,
                text=f"Welcome, {app_context.username} - Let's practice some Instrument today!",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_CURRENT_STREAK,
                text=f"Current Streak: {app_context.current_streak} day(s)",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_HIGHEST_STREAK,
                text=f"Highest Streak: {app_context.highest_streak} day(s)",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_DAILY_AVERAGE,
                text=f"Daily Average: {app_context.daily_average} minutes",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.PROFILE_USERNAME,
                text=app_context.username,
                action=Actions.LABEL_SET,
                source=ViewState.PROFILE,
            ),
            Signal(
                item=Items.PROFILE_EMAIL,
                text=app_context.email,
                action=Actions.LABEL_SET,
                source=ViewState.PROFILE,
            ),
        ]
