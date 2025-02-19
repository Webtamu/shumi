from views.view import View  
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QObject, pyqtSlot
from helpers.signals import Signal
from helpers.helpers import ViewState, Items

class NavigationRouter(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.theStackedWidget = QStackedWidget()
        self.theViewMap = {}
        self.theCounter = 0
     
    def addViews(self, aViewList: list[View]):
        for view in aViewList:
            self.theStackedWidget.addWidget(view.theWindow)
            self.theViewMap[view.theViewState] = self.theCounter
            self.theCounter += 1
            view.theNavSignal.connect(self._handleViewResponses)

    def navigateTo(self, aViewState: ViewState):
        if aViewState in self.theViewMap:
            self.theStackedWidget.setCurrentIndex(self.theViewMap[aViewState])

    def getCurrentView(self):
        return self.theStackedWidget.currentWidget()

    def doShow(self):
        self.theStackedWidget.show()
    
    @pyqtSlot(Signal)
    def _handleViewResponses(self, aSignal: Signal) -> None:
        theNavMap = {
            Items.SETTINGS : ViewState.SETTINGS,
            Items.HOME     : ViewState.HOME,
            Items.STATS    : ViewState.STATS,
            Items.PROFILE  : ViewState.PROFILE
        }
        theDestination = theNavMap.get(aSignal.theItem)

        if aSignal.theDebugTag and theDestination:
            print(f"Navigating to {theDestination}...")

        self.navigateTo(theDestination)


