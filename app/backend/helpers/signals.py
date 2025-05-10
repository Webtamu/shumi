from dataclasses import dataclass
from typing import Optional

from ..helpers import Items, Actions, ViewState, Colors


@dataclass
class Signal:
    action: Actions = Actions.DEFAULT
    item: Items = Items.DEFAULT
    state: Optional[bool] = None
    text: Optional[str] = None
    data: dict = None
    web: dict = None
    source: ViewState = ViewState.DEFAULT
    nav: bool = False

    def __str__(self):
        return (f"ActionType={Colors.CYAN}{self.action}{Colors.RESET}, "
                f"Item={Colors.CYAN}{self.item}{Colors.RESET}, "
                f"State={Colors.CYAN}{self.state}{Colors.RESET}, "
                f"Text={Colors.CYAN}'{self.text}'{Colors.RESET}, "
                f"Data={Colors.CYAN}'{self.data}'{Colors.RESET}, "
                f"Web={Colors.CYAN}'{self.web}'{Colors.RESET}, "
                f"Source={Colors.CYAN}{self.source}{Colors.RESET}, "
                f"Nav={Colors.CYAN}{self.nav}{Colors.RESET}")
