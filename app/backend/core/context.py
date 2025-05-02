# core/event_bus.py
from dataclasses import dataclass


@dataclass
class Context:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.email = None
        self.current_streak = 0
        self.highest_streak = 0
        self.daily_average = 0


app_context = Context()
