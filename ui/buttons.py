from PyQt6.QtWidgets import QPushButton

# Storage for pyqt button definitions
class cStartButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Start Session", aParent)
        self.setCheckable(True)
        # TODO: Refactor event handler into controller
        self.clicked.connect(self.doPrint)
    
    def doPrint(self):
        print("doStart!")

class cSettingsButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Settings", aParent)
        # TODO: Refactor event handler into controller
        self.clicked.connect(self.doPrint)
    
    def doPrint(self):
        print("doSettings!")


class cProfileButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Profile", aParent)
        # TODO: Refactor event handler into controller
        self.clicked.connect(self.doPrint)
    
    def doPrint(self):
        print("doProfile!")