class Signal():
    def __init__(self, anActionType: str="", anItemName: str="", aState: bool=False, aText: str="") -> None:
        self.theActionType = anActionType
        self.theItemName = anItemName
        self.theState = aState
        self.theText = aText
