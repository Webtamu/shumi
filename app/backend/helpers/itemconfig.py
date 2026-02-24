from dataclasses import dataclass


@dataclass
class ItemConfig:
    text: str = ""
    state: bool = False
    nav: bool = False
