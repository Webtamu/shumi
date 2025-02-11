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
     
    def addView(self, aViewState: ViewState, aView: View):
        self.theStackedWidget.addWidget(aView.theWindow)
        self.theViewMap[aViewState] = self.theCounter
        self.theCounter += 1
        aView.theNavSignal.connect(self._handleViewResponse)

    def navigateTo(self, aViewState: ViewState):
        if aViewState in self.theViewMap:
            self.theStackedWidget.setCurrentIndex(self.theViewMap[aViewState])

    def getCurrentView(self):
        return self.theStackedWidget.currentWidget()

    def doShow(self):
        self.theStackedWidget.show()
    
    @pyqtSlot(Signal)
    def _handleViewResponse(self, aSignal: Signal) -> None:
        theNavMap = {
            Items.SETTINGS: ViewState.SETTINGS,
            Items.HOME : ViewState.HOME
        }
        theDestination = theNavMap.get(aSignal.theItem)
        self.navigateTo(theDestination)

    @pyqtSlot(str, bool, str)
    def _handleModelResponse(self, aButtonName: str, aState: bool, aText: str) -> None:
        pass

