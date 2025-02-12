from dataclasses import dataclass
from helpers.helpers import Items, Actions, ViewState

@dataclass
class Signal():
    theActionType: Actions
    theItem: Items
    theState: bool 
    theText: str
    theSource: ViewState
