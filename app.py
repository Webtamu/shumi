from models.models import cModel
from views.home_view import cHomeView
from controllers.controllers import cHomeController
from PyQt6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, anArgs=[]):
        super().__init__(anArgs)
        self.theModel = cModel()
        self.theView = cHomeView()
        self.theController = cHomeController()
        self.theController.doConnectMVC(self.theModel, self.theView)
  
        self.theView.show()