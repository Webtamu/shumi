from .models import Model
from ..helpers import Signal, Items, ItemConfig, Logger


class ApplicationModel(Model):
    """
    This class houses temporary application metadata.
    """

    def __init__(self) -> None:
        super().__init__()

        # TEMP APP DATA STORE
        self.data_map: dict[Items, ItemConfig] = {
            Items.HOME: ItemConfig(
                text="Return Home",
                nav=True
            ),
            Items.SETTINGS: ItemConfig(
                text="Settings",
                nav=True
            ),
            Items.PROFILE: ItemConfig(
                text="Profile",
                nav=True
            ),
            Items.STATS: ItemConfig(
                text="Stats",
                nav=True
            ),
            Items.REPORT_BUG: ItemConfig(
                text="Report a Bug",
            ),
            Items.CONTACT: ItemConfig(
                text="Contact Us"
            ),
            Items.ABOUT: ItemConfig(
                text="About"
            ),
            Items.LOGIN_CREATE_ACCOUNT: ItemConfig(
                text="Create account",
                nav=True
            ),
            Items.CREATE_ACCOUNT_ALREADY_HAVE_ACCOUNT: ItemConfig(
                text="Already have an account? Sign in",
                nav=True
            ),
        }

    # Update data store and notify controller
    def update_model(self, signal: Signal) -> None:
        if action := self.action_map.get(signal.item):
            action()

        item_entry = self.data_map[signal.item]

        item_entry.state = not item_entry.state
        signal.text = item_entry.text
        signal.state = item_entry.state
        signal.nav = item_entry.nav
        Logger.debug(signal)
        self.model_signal.emit(signal)
