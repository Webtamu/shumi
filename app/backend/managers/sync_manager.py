from ..helpers import Logger, Signal, Items, Actions, ViewState
from ..services import DuckDBService, SupabaseService
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

        if not unsynced_rows:
            Logger.info('No unsynced sessions to upload.')
            return

        synced_rows = self.cloud_database.upload_unsynced_sessions(unsynced_rows)

        if synced_rows:
            self.local_database.mark_as_synced(synced_rows)
            Logger.info(f'Synced {len(synced_rows)} session(s) to Supabase.')
        else:
            Logger.error('Failed to sync any sessions.')

    def sync_from_cloud(self) -> None:
        """
        Sync cloud data to local DuckDB.
        """
        return

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
