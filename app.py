from models.home_model import HomeModel
from views.home_view import HomeView
from controllers.home_controller import HomeController
from PyQt6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, anArgs) -> None:
        super().__init__(anArgs)
        self.theHomeController = HomeController(HomeModel(), HomeView())