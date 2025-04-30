from ..helpers import Signal, Items, Actions, ViewState
from ..services import DuckDBService
from ..core.eventbus import event_bus


class ContextManager:
    def __init__(self, local_database: DuckDBService = None):
        # User-related context
        self.user_id = None
        self.username = None
        self.email = None

        # Stats fields
        self.current_streak = 0
        self.highest_streak = 0
        self.daily_average = 0  # In minutes
        self.local_database = local_database

    def refresh_fields(self):
        signals = self.generate_field_signals()
        for signal in signals:
            event_bus.publish(signal)

    def update_fields(self, field_dict: dict):
        for key, value in field_dict.items():
            setattr(self, key, value)

    def update_stats(self):
        self.current_streak = self.local_database.get_current_streak(self.user_id, "UTC")
        self.highest_streak = self.local_database.get_highest_streak(self.user_id, "UTC")
        self.daily_average = self.local_database.get_average_session_minutes(self.user_id)

    def generate_field_signals(self) -> list[Signal]:
        return [
            Signal(
                item=Items.HOME_WELCOME,
                text=f"Welcome, {self.username} - Let's practice some Instrument today!",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_CURRENT_STREAK,
                text=f"Current Streak: {self.current_streak} day(s)",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_HIGHEST_STREAK,
                text=f"Highest Streak: {self.highest_streak} day(s)",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.HOME_DAILY_AVERAGE,
                text=f"Daily Average: {self.daily_average} minutes",
                action=Actions.LABEL_SET,
                source=ViewState.HOME,
            ),
            Signal(
                item=Items.PROFILE_USERNAME,
                text=self.username,
                action=Actions.LABEL_SET,
                source=ViewState.PROFILE,
            ),
            Signal(
                item=Items.PROFILE_EMAIL,
                text=self.email,
                action=Actions.LABEL_SET,
                source=ViewState.PROFILE,
            ),
        ]
