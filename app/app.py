from PyQt6.QtWidgets import QApplication

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

from .backend.controllers.app_controller import ApplicationController
from .backend.routers.navigation_router import NavigationRouter

from .backend.helpers.logger import Logger
from .backend.helpers.enums import ViewState


class App(QApplication):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.model_list = [
            ApplicationModel(),
            PreferencesModel(),
            DataModel()
        ]
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

        self.navigation_router = NavigationRouter()
        self.initialize_views()

    def initialize_views(self):
        self.navigation_router.add_views(self.view_list)
        self.navigation_router.navigate_to(ViewState.LOGIN)
        self.navigation_router.do_show()

    def __del__(self):
        Logger.info("Closing Application, saving data!")
