from enum import Enum, auto

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

class Items(Enum):
    # LOGIN VIEW ITEMS
    LOGIN_USERNAME = auto()
    LOGIN_PASSWORD = auto()
    LOGIN_STAY_SIGNED_IN = auto()
    LOGIN_LOGIN = auto()
    LOGIN_CREATE_ACCOUNT = auto()
    LOGIN_CANT_SIGN_IN = auto()

    # CREATE ACCOUNT VIEW ITEMS
    CREATE_ACCOUNT_USERNAME = auto()         
    CREATE_ACCOUNT_PASSWORD = auto()         
    CREATE_ACCOUNT_PASSWORD_CONFIRM = auto()  
    CREATE_ACCOUNT_EMAIL = auto()             
    CREATE_ACCOUNT_CREATE = auto()
    CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT = auto()

    ABOUT = auto()
    BEGIN_TAKE = auto()
    CONTACT = auto()
    DARK_MODE = auto()
    DEFAULT = auto()
    HOME = auto()
    LANGUAGE = auto()
    
    PROFILE = auto()
    REPORT_BUG = auto()
    SETTINGS = auto()
    START = auto()
    STATS = auto()
    
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

class Actions(Enum):
    BTN_PRESS = auto()
    BOX_CHECK = auto()
    LIST_SET = auto()
    BROWSE_SET = auto()
    LABEL_SET = auto()
    LABEL_PRESS = auto()
    NONE = auto()
    DEFAULT = auto()

class Colors(Enum):
    RESET = "\033[0m"
    YELLOW = "\033[33m"
    BRIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"

    def __str__(self):
        return self.value
