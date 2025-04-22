from models.models import Model
from helpers.signals import Signal
from helpers.helpers import Items
from helpers.logger import Logger


class ApplicationModel(Model):
    """
    This class houses temporary application metadata.
    """

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.data_map = {
            Items.HOME: {"state": False,
                         "text": "Return Home",
                         "nav": True},

            Items.SETTINGS: {"state": False,
                             "text": "Settings",
                             "nav": True},

            Items.PROFILE: {"state": False,
                            "text": "Profile",
                            "nav": True},

            Items.STATS: {"state": False,
                          "text": "Stats",
                          "nav": True},

            Items.REPORT_BUG: {"state": False,
                               "text": "Report a Bug",
                               "nav": False},

            Items.CONTACT: {"state": False,
                            "text": "Contact Us",
                            "nav": False},

            Items.ABOUT: {"state": False,
                          "text": "About",
                          "nav": False},

            Items.BEGIN_TAKE: {"state": False,
                               "text": "Begin Take",
                               "nav": True},

            Items.LOGIN_CREATE_ACCOUNT: {"state": False,
                                         "text": "Create account",
                                         "nav": True},

            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT: {"state": False,
                                                        "text": "Already have an account? Sign in",
                                                        "nav": True},
        }

        self.action_map = {}
        self.thread = None
        self.model_type = "Application"

    # Update data store and notify controller
    def update_model(self, signal: Signal) -> None:
        if action := self.action_map.get(signal.item):
            action()

        item_entry = self.data_map[signal.item]

        item_entry["state"] = not item_entry["state"]
        signal.text = item_entry["text"]
        signal.state = item_entry["state"]
        signal.nav = item_entry["nav"]

        if signal.debug:
            Logger.info(f'{self.model_type} Model Handled: {signal}')

        self.model_signal.emit(signal)
