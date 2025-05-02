from PyQt6.QtCore import QSettings
from ..helpers import Timer, Signal
from ..services import DuckDBService
from ..core.eventbus import event_bus
from ..core.context import app_context
import os

# TODO: Move to config file
USER_DEFINED_TIME_PERIOD = 10
QSETTINGS_ORG = "WEBTAMU"
QSETTINGS_APP = "SHUMI"
QSETTINGS_STORAGE_KEY = "storage_directory"


class SessionManager:
    def __init__(self, local_database: DuckDBService):
        self.local_database = local_database
        self.timer = Timer(USER_DEFINED_TIME_PERIOD)
        self.timer.timer_signal.connect(event_bus.publish)
        self.timer.start()

    def add_session(self, user_id, start_time, stop_time) -> None:
        self.local_database.insert_data(user_id, start_time, stop_time)

    def begin_timer(self, signal: Signal) -> None:
        if self.timer:
            self.timer.start_timer(USER_DEFINED_TIME_PERIOD)

    def stop_timer(self, signal: Signal) -> None:
        if self.timer:
            self.timer.stop()
            self.add_session(app_context.user_id,
                             self.timer.start_time,
                             self.timer.stop_time)

    def save_session_notes(self, signal: Signal) -> None:
        self.settings = QSettings(QSETTINGS_ORG, QSETTINGS_APP)
        self.current_path = self.settings.value(QSETTINGS_STORAGE_KEY, defaultValue="")
        notes = signal.data.get("notes")
        if self.current_path and notes:
            try:
                os.makedirs(self.current_path, exist_ok=True)
                timestamp = self.timer.stop_time.strftime("%Y-%m-%d at %H-%M")
                file_path = os.path.join(self.current_path, f"{timestamp}.txt")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(notes)
            except Exception as e:
                print(f"Failed to save notes: {e}")
