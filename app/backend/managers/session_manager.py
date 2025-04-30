from ..helpers import Timer, Signal
from ..services import DuckDBService
from ..managers import ContextManager
from ..core.eventbus import event_bus
USER_DEFINED_TIME_PERIOD = 10


class SessionManager:
    def __init__(self, local_database: DuckDBService, context: ContextManager):
        self.local_database = local_database
        self.context = context
        self.timer = Timer(USER_DEFINED_TIME_PERIOD)
        self.timer.timer_signal.connect(event_bus.publish)
        self.timer.start()

    def add_session(self, user_id, start_time, stop_time) -> None:
        self.local_database.insert_data(user_id, start_time, stop_time)

    def begin_timer(self, signal: Signal) -> None:
        signal.nav = True
        if self.timer:
            self.timer.start_timer(USER_DEFINED_TIME_PERIOD)

    def stop_timer(self, signal: Signal) -> None:
        signal.nav = True
        if self.timer:
            self.timer.stop()
            self.add_session(self.context.user_id,
                             self.timer.start_time,
                             self.timer.stop_time)

            self.context.update_stats()
            self.context.refresh_fields()
