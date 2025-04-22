from PyQt6.QtCore import QThread, pyqtSignal
import time
import datetime

from helpers.signals import Signal
from helpers.helpers import Items, ViewState, Actions


class Timer(QThread):
    timer_signal = pyqtSignal(Signal)
    model_signal = pyqtSignal(Signal)

    def __init__(self, time_limit: int) -> None:
        super(Timer, self).__init__()
        self.time_limit = time_limit
        self.is_running = True
        self.start_time = None
        self.stop_time = None

    def run(self) -> None:
        """Run the countdown timer in a separate thread."""
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
        remaining_time = self.time_limit

        while remaining_time >= 0 and self.is_running:
            # Emit signal to update UI with remaining time
            self.timer_signal.emit(Signal(
                text=f"{remaining_time:02}",  # Format with leading zeros
                item=Items.TIMER,
                action=Actions.LABEL_SET,
                source=ViewState.SESSION
            ))
            time.sleep(1)
            remaining_time -= 1

        # Once the timer finishes, emit signal to notify the UI
        self.timer_signal.emit(Signal(
            item=Items.STOP,
            action=Actions.LABEL_SET,
            source=ViewState.SESSION,
            data=[]
        ))

    def stop(self) -> None:
        """Stop the countdown and record the stop time."""
        self.stop_time = datetime.datetime.now(datetime.timezone.utc)
        self.is_running = False  # Set is_running to False to break the loop
