from enum import Enum, auto
from PyQt6.QtCore import Qt


class StatusCodes(Enum):
    # Core-related error codes
    CORE_OK = 1000
    CORE_INVALID_INPUT = 1001
    CORE_DB_FAILURE = 1002
    CORE_RECORDING_FAILURE = 1003
    CORE_UPLOAD_FAILED = 1004
    CORE_DATA_SYNC_ERROR = 1005
    CORE_PRACTICE_LOG_ERROR = 1006

    # Side-related error codes
    SIDE_PET_DEATH = 2000
    SIDE_NOTIFICATION_FAILURE = 2001
    SIDE_METRONOME_ERROR = 2002
    SIDE_HOSTAGE_MODE_LOCK = 2003
    SIDE_TIKTOK_REDIRECTION = 2004

    # Storage-related error codes
    STORAGE_SAVE_ERROR = 3000
    STORAGE_LOAD_ERROR = 3001
    STORAGE_CLOUD_SYNC_ERROR = 3002
    STORAGE_EXPORT_ERROR = 3003
    STORAGE_IMPORT_ERROR = 3004

    # Authentication-related error codes
    AUTH_LOGIN_FAILED = 4000
    AUTH_PERMISSION_DENIED = 4001
    AI_PET_UNRESPONSIVE = 4002
    AI_AGENT_FAILURE = 4003
    SOCIAL_POST_FAILURE = 4004
    SOCIAL_FRIEND_SYNC_ERROR = 4005


class KeyAction(Enum):
    PRESS_ENTER = Qt.Key.Key_Return
    PRESS_ESCAPE = Qt.Key.Key_Escape
    PRESS_TAB = Qt.Key.Key_Tab
    PRESS_S = Qt.Key.Key_S


class Items(Enum):
    # LOGIN VIEW ITEMS
    LOGIN_USERNAME = auto()
    LOGIN_PASSWORD = auto()
    LOGIN_STAY_SIGNED_IN = auto()
    LOGIN_LOGIN = auto()
    LOGIN_CREATE_ACCOUNT = auto()
    LOGIN_CANT_SIGN_IN = auto()

    # HOME VIEW ITEMS
    HOME_HEATMAP = auto()

    # CREATE ACCOUNT VIEW ITEMS
    CREATE_ACCOUNT_USERNAME = auto()
    CREATE_ACCOUNT_PASSWORD = auto()
    CREATE_ACCOUNT_PASSWORD_CONFIRM = auto()
    CREATE_ACCOUNT_EMAIL = auto()
    CREATE_ACCOUNT_CREATE = auto()
    CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT = auto()

    # HOME VIEW ITEMS
    HOME_WELCOME = auto()
    HOME_CURRENT_STREAK = auto()
    HOME_HIGHEST_STREAK = auto()
    HOME_DAILY_AVERAGE = auto()

    # PROFILE VIEW ITEMS
    PROFILE_USERNAME = auto()
    PROFILE_EMAIL = auto()
    PROFILE_LOGOUT = auto()

    # SETTINGS VIEW ITEMS
    DARK_MODE = auto()
    SETTINGS_PATH = auto()
    SETTINGS_PATH_SELECTED = auto()
    SETTINGS_INPUT_DEVICE = auto()
    SETTINGS_OUTPUT_DEVICE = auto()
    REPORT_BUG = auto()
    ABOUT = auto()
    CONTACT = auto()
    LANGUAGE = auto()

    BEGIN_TAKE = auto()
    DEFAULT = auto()

    # SUMMARY VIEW ITEMS
    SUMMARY_NOTES = auto()

    # STATS VIEW ITEMS
    STATS_GRAPH = auto()

    # NAVIGATION ITEMS
    HOME = auto()
    PROFILE = auto()
    SETTINGS = auto()
    STATS = auto()

    START = auto()
    STOP = auto()
    SYNC = auto()
    TIME = auto()
    TIMER = auto()


class ViewState(Enum):
    HOME = auto()
    LOGIN = auto()
    SETTINGS = auto()
    PROFILE = auto()
    STATS = auto()
    SESSION = auto()
    SUMMARY = auto()
    CREATE = auto()
    ALL = auto()
    DEFAULT = auto()
    NONE = auto()


class Actions(Enum):
    BTN_PRESS = auto()
    BOX_CHECK = auto()
    COMBO_SET = auto()
    LABEL_SET = auto()
    LABEL_PRESS = auto()
    WEB_BTN_PRESS = auto()
    WEB_HEATMAP_SET = auto()
    NONE = auto()
    DEFAULT = auto()
