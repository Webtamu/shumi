from ..helpers import Timer, Signal
from ..services import DuckDBService
from ..managers import ContextManager
from typing import Callable

USER_DEFINED_TIME_PERIOD = 10


class SessionManager:
    def __init__(self, local_database: DuckDBService, callback: Callable, context: ContextManager):
        self.local_database = local_database
        self.timer = None
        self.callback = callback
        self.context = context

    def add_session(self, user_id, start_time, stop_time) -> None:
        self.local_database.insert_data(user_id, start_time, stop_time)

    def begin_timer(self, signal: Signal) -> None:
        signal.nav = True
        self.timer = Timer(USER_DEFINED_TIME_PERIOD)
        self.timer.timer_signal.connect(self.callback)
        self.timer.start()

    def stop_timer(self, signal: Signal) -> None:
        signal.nav = True
        if self.timer:
            self.timer.stop()
            self.add_session(self.context.user_id,
                             self.timer.start_time,
                             self.timer.stop_time)
            self.timer = None
