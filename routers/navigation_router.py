from views.view import View  
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QObject, pyqtSlot

class NavigationRouter(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.theStackedWidget = QStackedWidget()
        self.theViewMap = {}
        self.theCounter = 0
     
    def addView(self, aViewName: str, aView: View):
        self.theStackedWidget.addWidget(aView.theWindow)
        self.theViewMap[aViewName] = self.theCounter
        self.theCounter += 1
        aView.theNavSignal.connect(self._handleViewResponse)

    def navigateTo(self, aViewName: str):
        if aViewName in self.theViewMap:
            self.theStackedWidget.setCurrentIndex(self.theViewMap[aViewName])

    def getCurrentView(self):
        return self.theStackedWidget.currentWidget()

    def doShow(self):
        self.theStackedWidget.show()
    
    @pyqtSlot(str)
    def _handleViewResponse(self, aButtonName: str) -> None:
        if aButtonName == "btnSettings":
            self.navigateTo("viewSettings")
        elif aButtonName == "btnHome":
            self.navigateTo("viewHome")
        return None

    @pyqtSlot(str, bool, str)
    def _handleModelResponse(self, aButtonName: str, aState: bool, aText: str) -> None:
        pass

