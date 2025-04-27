import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt + TypeScript")
        self.browser = QWebEngineView()
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        html_path = os.path.join(script_dir, "index.html")

        self.browser.setUrl(QUrl.fromLocalFile(html_path))  # Update with the actual path to the HTML file
        self.setCentralWidget(self.browser)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
