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
