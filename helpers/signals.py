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