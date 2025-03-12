from dataclasses import dataclass
from helpers.helpers import Items, Actions, ViewState, Colors

@dataclass
class Signal():
    theActionType: Actions = Actions.DEFAULT
    theItem: Items = Items.DEFAULT
    theState: bool = False
    theText: str = ""
    theSource: ViewState = ViewState.DEFAULT
    theDebugTag: bool = True

    def __str__(self):
        return (f"ActionType={Colors.CYAN}{self.theActionType}{Colors.RESET}, "
                f"Item={Colors.CYAN}{self.theItem}{Colors.RESET}, "
                f"State={Colors.CYAN}{self.theState}{Colors.RESET}, "
                f"Text={Colors.CYAN}'{self.theText}'{Colors.RESET}, "
                f"Source={Colors.CYAN}{self.theSource}{Colors.RESET}")
