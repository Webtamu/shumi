from PyQt6.QtWidgets import QApplication

from models.application_model import ApplicationModel
from models.preferences_model import PreferencesModel
from models.data_model import DataModel

from views.login_view import LoginView
from views.create_view import CreateView
from views.home_view import HomeView
from views.settings_view import SettingsView
from views.stats_view import StatsView
from views.profile_view import ProfileView
from views.session_view import SessionView
from views.summary_view import SummaryView

from controllers.app_controller import ApplicationController
from routers.navigation_router import NavigationRouter

from helpers.logger import Logger
from helpers.helpers import ViewState

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
