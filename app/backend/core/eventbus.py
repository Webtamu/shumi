from queue import Queue, Empty
from ..helpers import Signal


class EventBus:
    def __init__(self):
        self._signal_queue: Queue[Signal] = Queue()

    def publish(self, *signals: Signal) -> None:
        for signal in signals:
            self._signal_queue.put(signal)

    def get_next_signal(self) -> Signal:
        try:
            return self._signal_queue.get_nowait()  # Safe + non-blocking
        except Empty:
            return None

    def has_signals(self) -> bool:
        return not self._signal_queue.empty()


# Singleton instance
event_bus = EventBus()
