from dataclasses import dataclass
from helpers.helpers import Items, Actions, ViewState

@dataclass
class Signal():
    theActionType: Actions = Actions.DEFAULT
    theItem: Items = Items.DEFAULT
    theState: bool = False
    theText: str = ""
    theSource: ViewState = ViewState.DEFAULT
    theBroadcastTag: bool = False
    theDebugTag: bool = True

    def __str__(self):
        return (f"Signal(ActionType={self.theActionType}, Item={self.theItem}, "
                f"State={self.theState}, Text='{self.theText}', "
                f"Source={self.theSource}, BroadcastTag={self.theBroadcastTag}, "
                f"DebugTag={self.theDebugTag})")
