from PyQt6.QtCore import QSettings

APPLICATION_NAME = "Shumi v1.0.0-beta"
QSETTINGS_ORG = "WEBTAMU"
QSETTINGS_APP = "SHUMI"
USER_DEFINED_TIME_PERIOD = 10
QSETTINGS_STORAGE_KEY = "storage_directory"
QSETTINGS_INPUT_DEVICE = "input_device"
QSETTINGS_OUTPUT_DEVICE = "output_device"
QSETTINGS_DARK_MODE_KEY = "dark_mode"
QSETTINGS_ACCESS_TOKEN = "access_token"
QSETTINGS_REFRESH_TOKEN = "refresh_token"
QSETTINGS_LAST_LOGIN = "last_login"


def get_settings() -> QSettings:
    return QSettings(QSETTINGS_ORG, QSETTINGS_APP)
