from models.application_model import ApplicationModel
from models.preferences_model import PreferencesModel
from models.data_model import DataModel

from views.home_view import HomeView
from views.settings_view import SettingsView
from views.stats_view import StatsView
from views.profile_view import ProfileView
from views.session_view import SessionView

from controllers.app_controller import ApplicationController

from routers.navigation_router import NavigationRouter
from PyQt6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, anArgs) -> None:
        super().__init__(anArgs)
        self.theModelList = [ApplicationModel(), PreferencesModel(), DataModel()]
        self.theViewList = [HomeView(), SettingsView(), StatsView(), ProfileView(), SessionView()]
        self.theApplicationController = ApplicationController(self.theModelList, self.theViewList)

        self.theNavigationRouter = NavigationRouter()
        self.initializeViews()
        

    def initializeViews(self):
        self.theNavigationRouter.addViews(self.theViewList)
        self.theNavigationRouter.theStackedWidget.setCurrentIndex(0)
        self.theNavigationRouter.doShow()

    def __del__(self):
        print("Closing Application, saving data!")