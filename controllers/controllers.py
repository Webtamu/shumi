from PyQt6.QtCore import QObject, pyqtSlot

class cHomeController(QObject):
    def __init__(self):
        super().__init__()
       
    # Connects to the model and view
    def doConnectMVC(self, aModel, aView):
        self._theModel = aModel
        self._theView = aView
        self._theModel.theButtonSignal.connect(self._handleModelResponse)
        aView.theStartButton.clicked.connect(lambda: self._handleViewResponse("btnStart"))
        aView.theSettingsButton.clicked.connect(lambda: self._handleViewResponse("btnSettings"))
        aView.theProfileButton.clicked.connect(lambda: self._handleViewResponse("btnProfile"))
    
    # Slot from View (Initial Trigger), sending to Model for processing
    @pyqtSlot(str)
    def _handleViewResponse(self, aButtonName):
        self._theModel.doUpdateButtonState(aButtonName)

    # Slot from Model (Compute Response), sending to View for presentation
    @pyqtSlot(str, bool, str)
    def _handleModelResponse(self, aButtonName, aState, aText):
        self._theView.doUpdateButtonUI(aButtonName, aState, aText)

    

