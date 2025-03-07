from enum import Enum, auto

class StatusCodes(Enum):

    CORE_OK = 1000  
    CORE_INVALID_INPUT = 1001  
    CORE_DB_FAILURE = 1002  
    CORE_RECORDING_FAILURE = 1003  
    CORE_UPLOAD_FAILED = 1004 
    CORE_DATA_SYNC_ERROR = 1005  
    CORE_PRACTICE_LOG_ERROR = 1006  

    SIDE_PET_DEATH = 2000  
    SIDE_NOTIFICATION_FAILURE = 2001  
    SIDE_METRONOME_ERROR = 2002  
    SIDE_HOSTAGE_MODE_LOCK = 2003  
    SIDE_TIKTOK_REDIRECTION = 2004  

    STORAGE_SAVE_ERROR = 3000  
    STORAGE_LOAD_ERROR = 3001  
    STORAGE_CLOUD_SYNC_ERROR = 3002  
    STORAGE_EXPORT_ERROR = 3003  
    STORAGE_IMPORT_ERROR = 3004  

    AUTH_LOGIN_FAILED = 4000  
    AUTH_PERMISSION_DENIED = 4001  
    AI_PET_UNRESPONSIVE = 4002  
    AI_AGENT_FAILURE = 4003  
    SOCIAL_POST_FAILURE = 4004  
    SOCIAL_FRIEND_SYNC_ERROR = 4005
    

 
class Items(Enum):

    HOME = auto()
    SETTINGS = auto()
    STATS = auto()
    PROFILE = auto()
    START = auto()
    STOP = auto()
    REPORT_BUG = auto()
    CONTACT = auto()
    ABOUT = auto()
    DARK_MODE = auto()
    LANGUAGE = auto()
    TIME = auto()
    DEFAULT = auto()

class ViewState(Enum):
    
    HOME = "viewHome"
    SETTINGS = "viewSettings"
    PROFILE = "viewProfile"
    STATS = "viewStats"
    SESSION = "viewSession"
    DEFAULT = auto()

class Actions(Enum):

    BTN_PRESS = auto()
    BOX_CHECK = auto()
    LIST_SET  = auto()
    BROWSE_SET = auto()
    DEFAULT = auto()
