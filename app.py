from models.home_model import HomeModel
from models.settings_model import SettingsModel
from views.home_view import HomeView
from views.settings_view import SettingsView
from helpers.helpers import ViewState
from controllers.home_controller import HomeController
from controllers.settings_controller import SettingsController
from routers.navigation_router import NavigationRouter
from PyQt6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, anArgs) -> None:
        super().__init__(anArgs)

        self.theHomeController = HomeController(HomeModel(), HomeView())
        self.theSettingsController = SettingsController(SettingsModel(), SettingsView())
        self.theNavigationRouter = NavigationRouter()
        self.initializeViews()
        

    def initializeViews(self):
        self.theNavigationRouter.addView(ViewState.HOME, self.theHomeController.theView)
        self.theNavigationRouter.addView(ViewState.SETTINGS, self.theSettingsController.theView)
        self.theNavigationRouter.theStackedWidget.setCurrentIndex(0)
        self.theNavigationRouter.doShow()

    def __del__(self):
        print("Closing Application, saving data!")