from PyQt6.QtWidgets import QPushButton

# Storage for PyQt button definitions


class StartButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__("Start Session", parent)
        self.setCheckable(True)


class SettingsButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__("Settings", parent)


class ProfileButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__("Profile", parent)
