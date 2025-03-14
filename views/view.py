from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from abc import abstractmethod

from helpers.signals import Signal
from helpers.helpers import Items, Actions, Colors, ViewState

class View(QWidget):  
    theNavSignal = pyqtSignal(Signal)

    @abstractmethod
    def __init__(self) -> None:
        self.theViewState = ViewState.DEFAULT
        self.theWindow = None
        super().__init__() 

    def updateView(self, aSignal: Signal) -> None:
        if aSignal.theItem == Items.DARK_MODE:
            self.toggleDarkMode(aSignal)

        theItemEntry = self.theItemMap.get(aSignal.theItem)
        if not theItemEntry:
            return  # Early exit if item not found

        theInstance = theItemEntry["instance"]
        self.updateWidget(theInstance, aSignal)

        if aSignal.theDebugTag:
            print(f"{Colors.YELLOW}Updated {aSignal.theItem} on {self.theViewState} to {aSignal.theState}{Colors.RESET}")

        self.theNavSignal.emit(aSignal)


    def updateWidget(self, anItem: QWidget, aSignal: Signal) -> None:
        self.theActionMap = {
            Actions.BTN_PRESS: self.updateButton,
            Actions.BOX_CHECK: self.updateBox,
            Actions.LABEL_SET: self.updateLabel
        }

        if theAction := self.theActionMap.get(aSignal.theActionType):
            theAction(anItem, aSignal)

    def toggleDarkMode(self, aSignal: Signal) -> None:
        if aSignal.theState: 
            with open("resources/dark_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
        else:
            with open("resources/light_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())
    
    def initializeStyle(self) -> None:
        with open("resources/light_mode.qss", "r") as file:
                self.theWindow.setStyleSheet(file.read())

    def updateButton(self, anItem: QWidget, aSignal: Signal) -> None:
        anItem.setChecked(aSignal.theState)
        anItem.setText(aSignal.theText)

    def updateBox(self, anItem: QWidget, aSignal: Signal) -> None:
        anItem.setChecked(aSignal.theState)
        anItem.setText(aSignal.theText)

    def updateLabel(self, anItem: QWidget, aSignal: Signal) -> None:
        anItem.setText(aSignal.theText)
