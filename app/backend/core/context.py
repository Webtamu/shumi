# core/event_bus.py
from dataclasses import dataclass


@dataclass
class Context:
    user_id: str = None
    username: str = None
    email: str = None
    current_streak: int = 0
    highest_streak: int = 0
    daily_average: float = 0


app_context = Context()
