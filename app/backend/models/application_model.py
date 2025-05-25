from .models import Model
from ..helpers import Signal, Items, Logger
from rust_ext import rust_hello


class ApplicationModel(Model):
    """
    This class houses temporary application metadata.
    """

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.data_map = {
            Items.HOME: {"state": False, "text": "Return Home", "nav": True},
            Items.SETTINGS: {"state": False, "text": "Settings", "nav": True},
            Items.PROFILE: {"state": False, "text": "Profile", "nav": True},
            Items.STATS: {"state": False, "text": "Stats", "nav": True},
            Items.REPORT_BUG: {"state": False, "text": "Report a Bug", },
            Items.CONTACT: {"state": False, "text": "Contact Us", },
            Items.ABOUT: {"state": False, "text": "About", },
            Items.LOGIN_CREATE_ACCOUNT: {"state": False, "text": "Create account", "nav": True},
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT: {"state": False, "text":
                                                        "Already have an account? Sign in",
                                                        "nav": True},
        }

        self.action_map = {Items.REPORT_BUG: rust_hello}

    # Update data store and notify controller
    def update_model(self, signal: Signal) -> None:
        if action := self.action_map.get(signal.item):
            action()

        item_entry = self.data_map[signal.item]

        item_entry["state"] = not item_entry["state"]
        signal.text = item_entry["text"]
        signal.state = item_entry["state"]
        signal.nav = item_entry.get("nav", False)

        Logger.debug(signal)
        self.model_signal.emit(signal)
