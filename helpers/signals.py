from dataclasses import dataclass
from typing import Optional

from helpers.helpers import Items, Actions, ViewState, Colors

@dataclass
class Signal():
    theActionType: Actions = Actions.DEFAULT
    theItem: Items = Items.DEFAULT
    theState: Optional[bool] = None  
    theText: Optional[str] = None
    theData: dict = None
    theSource: ViewState = ViewState.DEFAULT
    theDebugTag: bool = True
    theNavTag: bool = False

    def __str__(self):
        return (f"ActionType={Colors.CYAN}{self.theActionType}{Colors.RESET}, "
                f"Item={Colors.CYAN}{self.theItem}{Colors.RESET}, "
                f"State={Colors.CYAN}{self.theState}{Colors.RESET}, "
                f"Text={Colors.CYAN}'{self.theText}'{Colors.RESET}, "
                f"Data={Colors.CYAN}'{self.theData}'{Colors.RESET}, "
                f"Source={Colors.CYAN}{self.theSource}{Colors.RESET}, "
                f"Nav={Colors.CYAN}{self.theNavTag}{Colors.RESET}")  
