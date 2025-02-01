from PyQt6.QtWidgets import QPushButton

# Storage for pyqt button definitions
class cStartButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Start Session", aParent)
        self.setCheckable(True)
       
class cSettingsButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Settings", aParent)
        self.setCheckable(True)

class cProfileButton(QPushButton):
    def __init__(self, aParent=None):
        super().__init__("Profile", aParent)
        self.setCheckable(True)
