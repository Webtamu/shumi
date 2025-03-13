from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QObject

from views.view import View  
from helpers.signals import Signal
from helpers.helpers import ViewState, Items, Colors

class NavigationRouter(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.theStackedWidget = QStackedWidget()
        self.theViewMap: dict[ViewState, int] = {}
        self.theCounter = 0
     
    def addViews(self, aViewList: list[View]):
        for view in aViewList:
            self.theStackedWidget.addWidget(view.theWindow)
            self.theViewMap[view.theViewState] = self.theCounter
            self.theCounter += 1
            view.theNavSignal.connect(self.handleNavigation)

    def navigateTo(self, aViewState: ViewState):
        if aViewState in self.theViewMap:
            self.theStackedWidget.setCurrentIndex(self.theViewMap[aViewState])

    def getCurrentView(self):
        return self.theStackedWidget.currentWidget()

    def doShow(self):
        self.theStackedWidget.show()
    
    def handleNavigation(self, aSignal: Signal) -> None:
        theNavMap = {
            Items.SETTINGS : ViewState.SETTINGS,
            Items.HOME     : ViewState.HOME,
            Items.STATS    : ViewState.STATS,
            Items.PROFILE  : ViewState.PROFILE,
            Items.START    : ViewState.SESSION,
            Items.STOP     : ViewState.HOME
        }
        theDestination = theNavMap.get(aSignal.theItem)

        if not theDestination:
            return

        if aSignal.theDebugTag and theDestination:
            print(f"{Colors.BRIGHT_YELLOW}Navigating to {theDestination}...{Colors.RESET}")

        self.navigateTo(theDestination)


