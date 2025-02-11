from dataclasses import dataclass
from helpers.helpers import Items, Actions

@dataclass
class Signal():
    theActionType: Actions
    theItem: Items
    theState: bool 
    theText: str
