from PyQt6.QtWidgets import QApplication

from .backend.core import ApplicationController
from .backend.models import ApplicationModel, PreferencesModel, DataModel
from .backend.views import (
    LoginView,
    CreateView,
    HomeView,
    SettingsView,
    StatsView,
    ProfileView,
    SessionView,
    SummaryView,
)
from .backend.managers import NavigationManager, KeybindManager
from .backend.helpers import Logger, ViewState, Items, KeyAction


class App(QApplication):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.model_list = [
            ApplicationModel(),
            PreferencesModel(),
            DataModel()
        ]

        self.initialize_keybinds()

        self.view_list = [
            LoginView(),
            CreateView(),
            HomeView(),
            SettingsView(),
            StatsView(),
            ProfileView(),
            SessionView(),
            SummaryView()
        ]
        self.application_controller = ApplicationController(
            model_list=self.model_list,
            view_list=self.view_list
        )

        self.navigation_manager = NavigationManager()

        self.initialize_views()

    def initialize_views(self):
        for view in self.view_list:
            self.navigation_manager.add_view(view)
            KeybindManager.activate_keybinds(view)

        self.navigation_manager.navigate_to(ViewState.LOGIN)
        self.navigation_manager.do_show()

    def initialize_keybinds(self):
        KeybindManager.add_keybind(ViewState.LOGIN, KeyAction.PRESS_ENTER, Items.LOGIN_LOGIN)
        KeybindManager.add_keybind(ViewState.HOME, KeyAction.PRESS_S, Items.SETTINGS)

    def __del__(self):
        Logger.info("Closing Application, saving data!")
