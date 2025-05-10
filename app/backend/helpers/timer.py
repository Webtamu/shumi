from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition
import datetime

from ..helpers import Signal, Items, ViewState, Actions


class Timer(QThread):
    timer_signal = pyqtSignal(Signal)

    def __init__(self, time_limit: int) -> None:
        super(Timer, self).__init__()
        self.time_limit = time_limit
        self.start_time = None
        self.stop_time = None
        self.is_running = False
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()

    def run(self) -> None:
        while True:
            self.mutex.lock()
            while not self.is_running:
                self.wait_condition.wait(self.mutex)  # Sleep until start_timer() wakes
            self.start_time = datetime.datetime.now(datetime.timezone.utc)
            remaining_time = self.time_limit
            self.mutex.unlock()

            while remaining_time >= 0:
                self.timer_signal.emit(Signal(
                    text=f"{remaining_time:02}",
                    item=Items.TIMER,
                    action=Actions.LABEL_SET,
                    source=ViewState.SESSION
                ))

                self.mutex.lock()
                if not self.is_running:
                    self.mutex.unlock()
                    break

                self.wait_condition.wait(self.mutex, 1000)
                self.mutex.unlock()

                remaining_time -= 1

            # Timer finished or stopped, this signal is sent twice right now, once when we press stop timer,
            # and once when the timer expires.
            if self.is_running:
                self.timer_signal.emit(Signal(
                    item=Items.STOP,
                    action=Actions.LABEL_SET,
                    source=ViewState.SESSION,
                    data=[])
                )

    def start_timer(self, time_limit: int) -> None:
        self.mutex.lock()
        self.time_limit = time_limit
        self.is_running = True
        self.stop_time = None
        self.wait_condition.wakeAll()  # Wake up run() if sleeping
        self.mutex.unlock()

    def stop(self) -> None:
        self.mutex.lock()
        self.is_running = False
        self.mutex.unlock()

        self.wait_condition.wakeAll()
        self.stop_time = datetime.datetime.now(datetime.timezone.utc)
