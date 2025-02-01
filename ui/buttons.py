from PyQt6.QtWidgets import QPushButton

# Storage for pyqt button definitions
class StartButton(QPushButton):
    def __init__(self, aParent=None) -> None:
        super().__init__("Start Session", aParent)
        self.setCheckable(True)
       
class SettingsButton(QPushButton):
    def __init__(self, aParent=None) -> None:
        super().__init__("Settings", aParent)
        self.setCheckable(True)

class ProfileButton(QPushButton):
    def __init__(self, aParent=None) -> None:
        super().__init__("Profile", aParent)
     
