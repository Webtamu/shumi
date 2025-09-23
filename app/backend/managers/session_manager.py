from ..helpers import Timer, Signal, Logger, Actions, Items, ViewState
from ..services import DuckDBService
from ..core.eventbus import event_bus
from ..core.context import app_context
from ..core.settings import get_settings, QSETTINGS_STORAGE_KEY, USER_DEFINED_TIME_PERIOD
import os
import sounddevice
import numpy
import json
from scipy.io import wavfile


class SessionManager:
    def __init__(self, local_database: DuckDBService):
        self.local_database = local_database
        self.timer = Timer(USER_DEFINED_TIME_PERIOD)
        self.timer.timer_signal.connect(event_bus.publish)
        self.settings = get_settings()
        self.audio_buffer = []
        self.audio_stream = None
        self.timer.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            Logger.critical("Audio status:", status)
        self.audio_buffer.append(indata.copy())

    def add_session(self, user_id, start_time, stop_time) -> None:
        self.local_database.insert_data(user_id=user_id,
                                        start_time=start_time,
                                        stop_time=stop_time)

    def begin_session(self, signal: Signal) -> None:
        if self.timer:
            self.timer.start_timer(USER_DEFINED_TIME_PERIOD)

    def stop_session(self, signal: Signal) -> None:
        if self.timer:
            self.timer.stop()
            self.add_session(app_context.user_id,
                             self.timer.start_time,
                             self.timer.stop_time)

    def save_session_notes(self, signal: Signal) -> None:
        current_path = self.settings.value(QSETTINGS_STORAGE_KEY, defaultValue="")
        notes = signal.data.get("notes")
        if current_path and notes:
            try:
                os.makedirs(current_path, exist_ok=True)
                timestamp = self.timer.stop_time.strftime("%Y-%m-%d at %H-%M")
                file_path = os.path.join(current_path, f"{timestamp}.txt")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(notes)
            except Exception as e:
                Logger.critical(f"Failed to save notes: {e}")

    def get_session_data(self) -> list:
        sessions = self.local_database.fetch_data("session")
        parsed_sessions = []
        for s in sessions:
            parsed_sessions.append({
                "session_id": s["session_id"],
                "user_id": s["user_id"],
                "timestamp_start": s["timestamp_start"].isoformat(),
                "timestamp_stop": s["timestamp_stop"].isoformat(),
                "synced": s["synced"]
            })
        return parsed_sessions

    def update_web_components(self, signal: Signal) -> None:
        heatmap_signal = Signal(
                item=Items.HOME_HEATMAP,
                action=Actions.WEB_COMPONENT_SET,
                source=ViewState.HOME,
                )
        chart_signal = Signal(
                item=Items.STATS_GRAPH,
                action=Actions.WEB_COMPONENT_SET,
                source=ViewState.STATS,
                )
        event_bus.publish(heatmap_signal, chart_signal)

    def update_chart_data(self, signal: Signal) -> None:
        if signal.action == Actions.WEB_BTN_PRESS:
            return

        sessions = self.get_session_data()
        signal.data = json.dumps(sessions)
        signal.action = Actions.WEB_COMPONENT_SET

    def update_heatmap(self, signal: Signal) -> None:
        if signal.action == Actions.WEB_BTN_PRESS:
            return

        sessions = self.get_session_data()
        signal.data = json.dumps(sessions)
        signal.action = Actions.WEB_COMPONENT_SET
